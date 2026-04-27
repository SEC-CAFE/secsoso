#!/usr/bin/env bash
set -euo pipefail

usage(){
    cat <<'USAGE' 1>&2
Usage: deploy.sh -s {ui|appsearch} -e {test|prod} -t <deploy_dir> [--clean]

Examples:
  deploy.sh -s ui -e prod -t /data/www/secsoso.com --clean

Options:
  -s, --start       Required, service to deploy
  -e, --env         Required, runtime env: test/prod
  -t, --target_dir  Required, deploy target directory
  -c, --clean       Optional, delete target directory contents before deploy
USAGE
    exit 1
}

if ! command -v docker-compose >/dev/null 2>&1 && command -v docker >/dev/null 2>&1; then
    compose_cmd=(docker compose)
else
    compose_cmd=(docker-compose)
fi

ARGS=$(getopt -o s:e:t:c -l start:,env:,target_dir:,clean -- "$@")
eval set -- "$ARGS"

START=""
ENV=""
TARGET_DIR=""
CLEAN=""

while true; do
    case "$1" in
        -s|--start)
            case "$2" in
                ui|appsearch) START=$2; shift 2 ;;
                *) usage ;;
            esac
            ;;
        -e|--env)
            case "$2" in
                test|prod) ENV=$2; shift 2 ;;
                *) usage ;;
            esac
            ;;
        -t|--target_dir)
            TARGET_DIR=$2
            shift 2
            ;;
        -c|--clean)
            CLEAN=1
            shift
            ;;
        --)
            shift
            break
            ;;
        *)
            usage
            ;;
    esac
done

[ -n "$START" ] || usage
[ -n "$ENV" ] || usage
[ -n "$TARGET_DIR" ] || usage

TARGET_DIR=${TARGET_DIR%/}
ENV_FILE="test.env"
if [ "$ENV" = "prod" ]; then
    ENV_FILE="prod.env"
fi

init(){
    local compose_file=${1:-}
    mkdir -p "$TARGET_DIR"

    if [ -n "$compose_file" ] && [ -f "$TARGET_DIR/$compose_file" ]; then
        (
            cd "$TARGET_DIR"
            "${compose_cmd[@]}" -f "$compose_file" down || true
        )
    fi

    if [ -n "$CLEAN" ]; then
        rm -rf "$TARGET_DIR"/*
    fi
}

build_backend(){
    (
        cd ../backend
        docker build . -t secsoso_backend:1.0
    )
}

mount_and_reload_nginx(){
    local nginx_conf_dir=${NGINX_CONF_DIR:-}
    local nginx_site_conf_name=${NGINX_SITE_CONF_NAME:-secsoso.com.conf}
    local nginx_reload_container=${NGINX_RELOAD_CONTAINER:-nginx}

    if [ -z "$nginx_conf_dir" ]; then
        echo "NGINX_CONF_DIR not set, skip nginx conf mounting/reload"
        return
    fi

    mkdir -p "$nginx_conf_dir"
    cp -f "$TARGET_DIR/nginx/nginx.conf" "$nginx_conf_dir/$nginx_site_conf_name"

    if docker ps --format '{{.Names}}' | grep -q "^${nginx_reload_container}$"; then
        docker exec "$nginx_reload_container" nginx -s reload
    else
        echo "Nginx container '${nginx_reload_container}' not running, skip reload"
    fi
}

ui_deploy(){
    build_backend
    init "docker-compose.ui.yml"

    mkdir -p "$TARGET_DIR/html" "$TARGET_DIR/nginx" "$TARGET_DIR/backend/.envs"

    cp -f docker-compose.ui.yml "$TARGET_DIR/docker-compose.ui.yml"
    cp -rf ../backend/src "$TARGET_DIR/backend/"
    cp -f ../backend/main.py "$TARGET_DIR/backend/"
    cp -f ../backend/.envs/$ENV_FILE "$TARGET_DIR/backend/.envs/"
    cp -f ../backend/.envs/.env "$TARGET_DIR/backend/.envs/.env" 2>/dev/null || true

    # Deploy built frontend if dist exists, otherwise fallback to source for custom workflows.
    if [ -d ../frontend/dist ]; then
        cp -rf ../frontend/dist/* "$TARGET_DIR/html/"
    else
        cp -rf ../frontend/* "$TARGET_DIR/html/"
    fi

    cp -f nginx/ui_nginx.conf "$TARGET_DIR/nginx/nginx.conf"
    if [ "$ENV" = "prod" ]; then
        echo 'APP_ENV=prod' > "$TARGET_DIR/backend/.envs/.env"
    else
        echo 'APP_ENV=test' > "$TARGET_DIR/backend/.envs/.env"
    fi

    (
        cd "$TARGET_DIR"
        "${compose_cmd[@]}" -f docker-compose.ui.yml up -d
    )

    mount_and_reload_nginx
}

echo "Start deploy $START"
echo "DIR: $TARGET_DIR, ENV: $ENV, CLEAN: ${CLEAN:-0}"

case "$START" in
    ui)
        ui_deploy
        ;;
    appsearch)
        echo "Service '$START' is managed by docker compose files directly."
        usage
        ;;
    *)
        usage
        ;;
esac
