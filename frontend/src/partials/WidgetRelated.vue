<template>
  <div class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30  p-5">
    <div class="font-aspekta font-[650] mb-3">相关提问</div>
    <ul class="space-y-3" v-if="more_question_show">
      
      <li class="inline-flex" v-for="q in questions" :q="q">
        <span class="text-sky-500 mr-2">—</span> 
        <a class="font-aspekta font-[650] text-sm inline-flex relative hover:text-sky-500 duration-150 ease-out before:scale-x-0 before:origin-center before:absolute before:inset-0 before:bg-sky-200 dark:before:bg-sky-500 before:opacity-30 before:-z-10 before:translate-y-1/4 before:-rotate-2 hover:before:scale-100 before:duration-150 before:ease-in-out" href="#" @click="flush(q)">{{q}}</a>
      </li>
      
    </ul>
    <div v-else role="status" class="mt-1 py-5 border-t border-slate-100 dark:border-slate-800 grow text-sm text-slate-500 dark:text-slate-400 break-all animate-pulse">
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[460px] mb-2.5"></div>
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>                      
      <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
      <span class="sr-only">Loading...</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WidgetRelated',
  props: ['questions', 'more_question_show'],
  methods: {
    flush(q) {
      const currentRoute = this.$route;
      const newQuery = { ...currentRoute.query };
      delete newQuery['question'];
      const newPath = `${currentRoute.path}?question=${q}`;
      window.location.replace(newPath);
    }
  }
}
</script>