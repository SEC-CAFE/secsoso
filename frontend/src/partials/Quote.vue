<template>
  <article id="quote_box" style="display: none;" class="absolute rounded-lg bg-white z-50 dark:bg-slate-700 border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 shadow-lg dark:shadow-sky-950 px-5 mb-5 w-80 h-auo">
    <div class="items-start border-slate-100 dark:border-slate-800 pb-2">
        <div class="grow">
            <div class="text-sm text-slate-500 mt-3 mb-2 font-[650] line-clamp-1">
              {{ title }}
            </div>
            <div class="md:flex">
                <div  class="line-clamp-4 grow text-sm text-slate-500 dark:text-slate-400 break-all prose dark:prose-invert prose-strong:text-slate-500 prose-headings:text-slate-500">
                  {{content}}
                </div>
            </div>
        </div>
    </div>
    <div class="py-2 border-t border-slate-100 dark:border-slate-800 truncate">
        <a class="text-xs text-sky-500 no-underline" :href="url" target="_blank">{{ url }}</a>
    </div>
  </article>
</template>

<script>
export default {
  name: 'Quote',
  props: ['title', 'content', 'url'],
}
</script>