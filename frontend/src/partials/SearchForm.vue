<template>
  <section>
    <div class="absolute inset-0 min-h-[500px] flex items-center justify-center">
        <div class="relative flex flex-col gap-2 px-4 -mt-24 max-w-full w-[550px]">
            <div class="flex gap-4 items-center justify-center cursor-default select-none relative mb-8">
                <div class="w-auto">
                  <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M7 9.12739L24.0082 4L41 9.12739V19.6424C41 30.6945 34.153 40.5063 24.0025 44C13.8492 40.5064 7 30.6923 7 19.6376V9.12739Z" fill="none" stroke="#0284C7" stroke-width="3" stroke-linejoin="bevel"/>
                    <path d="M24 30C27.866 30 31 26.866 31 23C31 19.134 27.866 16 24 16C20.134 16 17 19.134 17 23C17 26.866 20.134 30 24 30Z" fill="none" stroke="#0284C7" stroke-width="3" stroke-linejoin="bevel"/>
                    <path d="M29 29L35 36" stroke="#0284C7" stroke-width="3" stroke-linecap="square" stroke-linejoin="bevel"/>
                    <path d="M41 19.6426C41 30.6946 34.153 40.5065 24.0024 44.0002" stroke="#0284C7" stroke-width="3" stroke-linejoin="bevel"/>
                  </svg>
                </div>
                <div class="text-center font-medium text-2xl md:text-3xl text-zinc-950 dark:text-white relative text-nowrap">SECSOSO 安全搜搜</div>
                <div class="transform scale-75 origin-left items-center rounded-full bg-gray-100 px-2 py-1 text-xs font-medium text-zinc-600 dark:bg-slate-700 dark:text-slate-100">beta</div>
            </div>
            <!--
            <div class="mb-4 flex items-center justify-center gap-2">
              <a href="#111" target="_blank" class="text-sm underline text-zinc-500 hover:text-amber-500 flex gap-2 items-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chrome ">
                    <circle cx="12" cy="12" r="10"></circle>
                    <circle cx="12" cy="12" r="4"></circle>
                    <line x1="21.17" x2="12" y1="8" y2="8"></line>
                    <line x1="3.95" x2="8.54" y1="6.06" y2="14"></line>
                    <line x1="10.88" x2="15.46" y1="21.94" y2="14"></line>
                </svg>
                Try Browser Extension
              </a>
            </div>
            -->
            <form action="/search" method="get">
              <label class="relative bg-white dark:bg-slate-700 flex items-center justify-center border dark:border-slate-800 focus-within:border-sky-500  py-2 px-2 rounded-full gap-2 " for="search-bar">
                <input name="question" id="search-bar" autofocus="" placeholder="Ask SECSOSO anything about security ..." class="px-2 pr-6 w-full rounded-md flex-1 outline-none bg-white dark:bg-slate-700 " value="">
                <button type="submit" class="w-auto py-1 px-2 bg-sky-500 hover:bg-sky-600  text-white fill-white active:scale-95 overflow-hidden relative rounded-xl">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right ">
                      <path d="M5 12h14"></path>
                      <path d="m12 5 7 7-7 7"></path>
                  </svg>
                </button>
              </label>
            </form>
            <div class="flex mt-4 gap-2 flex-wrap justify-center">
              <a title="怎么修复SQL注入?" class="border dark:border-none border-zinc-200/50 text-ellipsis overflow-hidden text-nowrap items-center rounded-full bg-slate-100 hover:bg-slate-200/80 dark:bg-slate-700 dark:text-slate-100 hover:text-zinc-950 px-2 py-1 text-xs font-medium text-zinc-600" href="/search?question=怎么修复SQL注入?">怎么修复SQL注入?</a>
              <a title="最新需要关注的漏洞?" class="border dark:border-none border-zinc-200/50 text-ellipsis overflow-hidden text-nowrap items-center rounded-full bg-slate-100 hover:bg-slate-200/80 dark:bg-slate-700 dark:text-slate-100 hover:text-zinc-950 px-2 py-1 text-xs font-medium text-zinc-600" href="/search?question=最新需要关注的漏洞?">最新需要关注的漏洞?</a>
              <a title="SECSOSO是什么?" class="border dark:border-none border-zinc-200/50 text-ellipsis overflow-hidden text-nowrap items-center rounded-full bg-slate-100 hover:bg-slate-200/80 dark:bg-slate-700 dark:text-slate-100 hover:text-zinc-950 px-2 py-1 text-xs font-medium text-zinc-600" href="/search?question=SECSOSO是什么?">SECSOSO是什么?</a>
            </div>
            <div class="text-center flex flex-col items-center text-xs text-zinc-500 gap-1 mt-4">
                <div class="flex gap-2 justify-center dark:text-slate-400">
                    <div>对SECSOSO有建议或反馈bug?</div>
                    <div>
                      <a class="text-sky-600 font-medium inline-flex gap-1 items-center flex-nowrap text-nowrap" href="mailto:f00y1n9@gmail.com">联系我们!</a>
                    </div>
                </div>
                
            </div>
        </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'SearchForm',
}
</script>