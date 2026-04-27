<template>
  <div class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5">
    <div class="flex items-center space-x-3 mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
        <path fill="#38BDF8" fill-rule="evenodd" d="M7.5 6v.75H5.513c-.96 0-1.764.724-1.865 1.679l-1.263 12A1.875 1.875 0 0 0 4.25 22.5h15.5a1.875 1.875 0 0 0 1.865-2.071l-1.263-12a1.875 1.875 0 0 0-1.865-1.679H16.5V6a4.5 4.5 0 1 0-9 0ZM12 3a3 3 0 0 0-3 3v.75h6V6a3 3 0 0 0-3-3Zm-3 8.25a3 3 0 1 0 6 0v-.75a.75.75 0 0 1 1.5 0v.75a4.5 4.5 0 1 1-9 0v-.75a.75.75 0 0 1 1.5 0v.75Z" clip-rule="evenodd" />
      </svg>
      <span class="text-xs text-slate-400 dark:text-slate-500">好书推荐</span>
    </div>
    <div class="text-center">
      <a href="https://s.click.taobao.com/D3ISYlt" target="_blank" title="套装 官网正版 红蓝攻防实战演练 共2册 红蓝攻防 构建实战化网络安全防御体系+ATT&CK视角下的红蓝对抗实战指南  ¥168">
        <img class="inline-flex" src="../images/ad1.jpeg" width="300"/>
        <!--<span class="text-xs">套装 官网正版 红蓝攻防实战演练 共2册 红蓝攻防 构建实战化网络安全防御体系+ATT&CK视角下的红蓝对抗实战指南</span>-->
      </a>
    </div>
  </div>

  <div class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5">
    <div class="flex items-center space-x-3 mb-2">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
        <path fill="#38BDF8" fill-rule="evenodd" d="M9 4.5a.75.75 0 0 1 .721.544l.813 2.846a3.75 3.75 0 0 0 2.576 2.576l2.846.813a.75.75 0 0 1 0 1.442l-2.846.813a3.75 3.75 0 0 0-2.576 2.576l-.813 2.846a.75.75 0 0 1-1.442 0l-.813-2.846a3.75 3.75 0 0 0-2.576-2.576l-2.846-.813a.75.75 0 0 1 0-1.442l2.846-.813A3.75 3.75 0 0 0 7.466 7.89l.813-2.846A.75.75 0 0 1 9 4.5ZM18 1.5a.75.75 0 0 1 .728.568l.258 1.036c.236.94.97 1.674 1.91 1.91l1.036.258a.75.75 0 0 1 0 1.456l-1.036.258c-.94.236-1.674.97-1.91 1.91l-.258 1.036a.75.75 0 0 1-1.456 0l-.258-1.036a2.625 2.625 0 0 0-1.91-1.91l-1.036-.258a.75.75 0 0 1 0-1.456l1.036-.258a2.625 2.625 0 0 0 1.91-1.91l.258-1.036A.75.75 0 0 1 18 1.5ZM16.5 15a.75.75 0 0 1 .712.513l.394 1.183c.15.447.5.799.948.948l1.183.395a.75.75 0 0 1 0 1.422l-1.183.395c-.447.15-.799.5-.948.948l-.395 1.183a.75.75 0 0 1-1.422 0l-.395-1.183a1.5 1.5 0 0 0-.948-.948l-1.183-.395a.75.75 0 0 1 0-1.422l1.183-.395c.447-.15.799-.5.948-.948l.395-1.183A.75.75 0 0 1 16.5 15Z" clip-rule="evenodd" />
      </svg>

      <span class="text-xs text-slate-400 dark:text-slate-500">AD</span>
    </div>
    <div class="text-center addGoogleItem">

      <ins class="adsbygoogle"
     style="display:inline-block;width:210px;height:400px"
     data-ad-client="ca-pub-9376316394747034"
     data-ad-slot="6589673396"></ins>
    </div>
  </div>


</template>

<script>
import { onMounted} from 'vue'

export default {
  name: 'WidgetAds',
  setup() {
    onMounted(() => {
      const oScript = document.createElement('script');
      oScript.type = 'text/javascript';
      oScript.async = true
      oScript.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9376316394747034';
      oScript.crossOrigin  = "anonymous"
      document.head.appendChild(oScript);

      window.addGoogleAds()
    });
  }
}
</script>
