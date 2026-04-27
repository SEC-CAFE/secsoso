<template>
  <article class="py-5 border-t border-slate-100 dark:border-slate-800">
    <div class="flex items-start">
      <div class="grow">
        <div class="text-xs text-slate-500 mb-1">
          <span class="text-sky-500 ">—</span>
          <span class="ml-1">{{ item.site }}</span>
          <!--
          <div class="float-right">SOURCES: 
            <div v-for="source in item.engines" :source="source" class="text-xs inline-flex font-medium  text-slate-500 ml-1">{{source}}</div>
          </div>
          -->
          <a  class="float-right text-xs inline-flex font-medium bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-100 rounded-full text-center px-2.5 py-1 ml-1" :href="'https://web.archive.org/web/'+item.url" target="_blank">快照</a>
          
        </div>
        <h3 class="font-aspekta text-lg font-[650] mb-1">
          <a class="inline-flex relative hover:text-sky-500 duration-150 ease-out before:scale-x-0 before:origin-center before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:translate-y-1/4 before:-rotate-2 hover:before:scale-100 before:duration-150 before:ease-in-out" :href="item.url" target="_blank">{{item.title}}</a>
        </h3>
        <div class="flex">
          <div class="grow text-sm text-slate-500 dark:text-slate-400">
            {{item.content}}
          </div>
        </div>        
      </div>
    </div>
  </article>
</template>

<script>
export default {
  name: 'ResultItem',
  props: ['item'],
}
</script>