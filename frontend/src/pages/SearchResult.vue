<template>
  <div class="max-w-7xl mx-auto">
    <div class="min-h-screen flex">

      <SideNavigation />

      <!-- Main content -->
      <main class="grow overflow-hidden px-6">
        <div class="w-full h-full max-w-[1072px] mx-auto flex flex-col">
          <!-- Content -->
          <!-- Back -->
          <div class="pt-12 md:pt-16 pb-8 md:pb-10">
            <div class="mb-3">
              <router-link class="inline-flex text-sky-500 rounded-full border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30" to="/">
                <span class="sr-only">Back</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="34" height="34">
                  <path class="fill-current" d="m16.414 17 3.293 3.293-1.414 1.414L13.586 17l4.707-4.707 1.414 1.414z" />
                </svg>
              </router-link>
            </div>
            <header>
              <div class="flex items-center justify-between mb-1">
                <!-- Post date -->
                <div class="text-xs text-slate-800 dark:text-slate-100 uppercase">
                  <!--
                  <span class="h3 font-aspekta mb-4">How to Control CSS Animations with JavaScript</span>
                  -->
                  <form action="/search" method="get" class="lg:w-[700px] md:w-[240px] text-lg ">
                    <label class="relative bg-white dark:bg-slate-700 flex items-center justify-center border dark:border-slate-800 focus-within:border-sky-500  py-2 px-2 rounded-full gap-2 " for="search-bar">
                      <input name="question" id="search-bar" autofocus="" placeholder="Ask SECSOSO anything about security ..." class="px-2 pr-6 w-full rounded-md flex-1 outline-none bg-white dark:bg-slate-700 " :value=question>
                      <button type="submit" class="w-auto py-1 px-2 bg-sky-500 hover:bg-sky-600  text-white fill-white active:scale-95 overflow-hidden relative rounded-xl">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right ">
                            <path d="M5 12h14"></path>
                            <path d="m12 5 7 7-7 7"></path>
                        </svg>
                      </button>
                    </label>
                  </form>
                </div>
                <!-- Share buttons -->
                <ul class="inline-flex">
                  <li>
                    <a class="flex justify-center items-center text-slate-400 dark:text-slate-500 hover:text-sky-500 dark:hover:text-sky-500 transition duration-150 ease-in-out" href="#0" aria-label="Twitter">
                      <svg class="w-8 h-8 fill-current" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                        <path d="M24 11.5c-.6.3-1.2.4-1.9.5.7-.4 1.2-1 1.4-1.8-.6.4-1.3.6-2.1.8-.6-.6-1.5-1-2.4-1-1.7 0-3.2 1.5-3.2 3.3 0 .3 0 .5.1.7-2.7-.1-5.2-1.4-6.8-3.4-.3.5-.4 1-.4 1.7 0 1.1.6 2.1 1.5 2.7-.5 0-1-.2-1.5-.4 0 1.6 1.1 2.9 2.6 3.2-.3.1-.6.1-.9.1-.2 0-.4 0-.6-.1.4 1.3 1.6 2.3 3.1 2.3-1.1.9-2.5 1.4-4.1 1.4H8c1.5.9 3.2 1.5 5 1.5 6 0 9.3-5 9.3-9.3v-.4c.7-.5 1.3-1.1 1.7-1.8z"></path>
                      </svg>
                    </a>
                  </li>
                  <li>
                    <a class="flex justify-center items-center text-slate-400 dark:text-slate-500 hover:text-sky-500 dark:hover:text-sky-500 transition duration-150 ease-in-out" href="#0" aria-label="Facebook">
                      <svg class="w-8 h-8 fill-current" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                        <path d="M14.023 24 14 17h-3v-3h3v-2c0-2.7 1.672-4 4.08-4 1.153 0 2.144.086 2.433.124v2.821h-1.67c-1.31 0-1.563.623-1.563 1.536V14H21l-1 3h-2.72v7h-3.257Z"></path>
                      </svg>
                    </a>
                  </li>
                  <li>
                    <a class="flex justify-center items-center text-slate-400 dark:text-slate-500 hover:text-sky-500 dark:hover:text-sky-500 transition duration-150 ease-in-out" href="#0" aria-label="Share">
                      <svg class="w-8 h-8 fill-current" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
                        <path d="M20 14c1.654 0 3-1.346 3-3s-1.346-3-3-3-3 1.346-3 3c0 .223.029.439.075.649l-3.22 2.012A2.97 2.97 0 0 0 12 13c-1.654 0-3 1.346-3 3s1.346 3 3 3a2.97 2.97 0 0 0 1.855-.661l3.22 2.012c-.046.21-.075.426-.075.649 0 1.654 1.346 3 3 3s3-1.346 3-3-1.346-3-3-3a2.97 2.97 0 0 0-1.855.661l-3.22-2.012c.046-.21.075-.426.075-.649 0-.223-.029-.439-.075-.649l3.22-2.012A2.97 2.97 0 0 0 20 14Z"></path>
                      </svg>
                    </a>
                  </li>
                </ul>
              </div>
            </header>
          </div>
          <div class="grow md:flex space-y-8 md:space-y-0 md:space-x-8 ">
            <!-- Middle area -->
            <div class="grow">
              <div class="max-w-[700px]">
                <article>
                  <div class="text-slate-500 dark:text-slate-400 space-y-8">
                    <article class="rounded-lg border border-slate-200 dark:border-slate-800 dark:bg-gradient-to-t dark:from-slate-800 dark:to-slate-800/30 p-5 mb-5">
                      <div class="absolute top-0 left-0 right-0 h-0.5 bg-sky-500" aria-hidden="true"></div>
                      <div class="items-start border-slate-100 dark:border-slate-800">
                          <div class="grow">
                              <div class="text-xs text-slate-500 mb-1">
                                <div class="text-xs inline-flex font-medium bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-100 rounded-full text-center px-2.5 py-1">AI回答</div>
                                <button v-if="!stop_receive_answer_tag && ai_answer_show" class="float-right text-xs inline-flex font-medium bg-sky-500 hover:bg-sky-600 text-white rounded-full text-center px-2.5 py-1" @click="stop_receive_answer">停止生成</button>
                              </div>
                              <div class="md:flex">
                                  <div v-if="ai_answer_show" class="grow text-sm text-slate-500 dark:text-slate-400 break-all prose max-w-none dark:prose-invert prose-strong:text-slate-500 prose-headings:text-slate-500">
                                    <Markdown :source="ai_answer" :linkify="true" :breaks="true" :highlight="{auto:true}" :html="true" />
                                    <quote :title="quote_title" :content="quote_content" :url="quote_url"/>
                                    
                                  </div>
                                  <div v-else role="status" class="mt-1 grow text-sm text-slate-500 dark:text-slate-400 break-all animate-pulse">
                                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[460px] mb-2.5"></div>
                                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>
                                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[300px] mb-2.5"></div>
                                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[400px] mb-2.5"></div>
                                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[200px] mb-2.5"></div>
                                    <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                                    <span class="sr-only">Loading...</span>
                                </div>
                              </div>
                          </div>
                          
                      </div>
                      <!--
                      <div class="px-1 pt-4">
                          <ul>
                              <li class="flex items-center py-1"><svg class="w-3 h-3 fill-current text-sky-500 mr-3 mt-1.5 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
                                      <path d="M10.28 2.28L3.989 8.575 1.695 6.28A1 1 0 00.28 7.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 2.28z"></path>
                                  </svg>
                                  <div class="text-sm"><a href="/url/Q8yR">Ghostscript本地代码执行漏洞（CVE-2024-29510）</a><span class="pl-1 text-xs text-slate-400 dark:text-slate-500">Seebug 漏洞平台</span></div>
                              </li>
                              <li class="flex items-center py-1"><svg class="w-3 h-3 fill-current text-sky-500 mr-3 mt-1.5 shrink-0" viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg">
                                      <path d="M10.28 2.28L3.989 8.575 1.695 6.28A1 1 0 00.28 7.695l3 3a1 1 0 001.414 0l7-7A1 1 0 0010.28 2.28z"></path>
                                  </svg>
                                  <div class="text-sm"><a href="/url/CmOW">Ghostscript 格式化字符串漏洞</a><span class="pl-1 text-xs text-slate-400 dark:text-slate-500">OSCS开源安全情报</span></div>
                              </li>
                          </ul>
                      </div>
                      -->
                    </article>
                    <div>
                        <ResultItem v-if="search_result_show" v-for="item in items" :key="item.id" :item="item" />
                        <div v-else v-for="item in [1,2,3,4,5]" role="status" class="mt-1 py-5 border-t border-slate-100 dark:border-slate-800 grow text-sm text-slate-500 dark:text-slate-400 break-all animate-pulse">
                          <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[460px] mb-2.5"></div>
                          <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px] mb-2.5"></div>
                          <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[330px] mb-2.5"></div>                      
                          <div class="h-2 bg-gray-200 rounded-full dark:bg-gray-700 max-w-[360px]"></div>
                          <span class="sr-only">Loading...</span>
                        </div>
                        <nav v-if="search_result_show" class="flex items-center justify-between border-t border-gray-200 dark:border-slate-600 py-3" aria-label="Pagination">
                          <div class="hidden sm:block">
                            <p class="text-sm text-gray-700 dark:text-slate-400">
                              {{ ' ' }}
                              <span class="font-medium">{{ items.length }}</span>
                              {{ ' ' }}
                              results
                              {{ 'in' }}
                              Page
                              {{ ' ' }}
                              <span class="font-medium">{{ pageno }}</span>
                            </p>
                          </div>
                          <div class="flex flex-1 justify-between sm:justify-end">
                            <a v-if="pageno>1" href="#" @click="prev_page" class="relative inline-flex items-center rounded-md bg-sky-500 hover:bg-sky-600 px-3 py-2 text-sm font-semibold text-white   focus-visible:outline-offset-0">Previous</a>
                            <a v-if="items.length>0" href="#" @click="next_page" class="relative ml-3 inline-flex items-center rounded-md bg-sky-500 hover:bg-sky-600 px-3 py-2 text-sm font-semibold text-white   focus-visible:outline-offset-0">Next</a>
                          </div>
                        </nav>
                        
                    </div>
                  </div>
                </article>
          
              </div>
            </div>
          
            <!-- Right sidebar -->
            <aside class="md:w-[240px] lg:w-[300px] shrink-0">
              <div class="space-y-6">
                <WidgetRelated  :questions="more_question" :more_question_show="more_question_show"/>
                <WidgetSponsor />
                <WidgetLinks />
                <Backtop />
            
              </div>
            </aside>
          
          </div>

          <Footer />

        </div>
      </main>

    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

import Markdown from 'vue3-markdown-it';
import 'highlight.js/styles/monokai.css';

import SideNavigation from '../partials/SideNavigation.vue'
import Header from '../partials/Header.vue'
import Footer from '../partials/Footer.vue'
import Backtop from '../components/Backtop.vue'
import ResultItem from '../partials/ResultItem.vue'
import Quote from '../partials/Quote.vue'

import WidgetRelated from '../partials/WidgetRelated.vue'
import WidgetLinks from '../partials/WidgetLinks.vue'
import WidgetSponsor from '../partials/WidgetSponsor.vue'

export default {
  name: 'SearchResult',
  components: {
    SideNavigation,
    Header,
    WidgetRelated,
    WidgetLinks,
    WidgetSponsor,
    ResultItem,
    Footer,
    Backtop,
    Quote,
    Markdown
  },
  data(){
    return {
      quote_title: '',
      quote_content: '',
      quote_url: '',
      _docClickHandler: null,
    }
  },
  created: function() {
    this._docClickHandler = (event) => {
      let element = event.target;
      let quote_el = document.getElementById('quote_box');
      if (!quote_el) {
        return;
      }
      let name = element.getAttribute('name');
      let _id = parseInt(element.getAttribute('quote_id'))-1;
      if (name != 'quote_number'){
        quote_el.style.display = 'none';
      }else{
        quote_el.style.left = '0px';
        quote_el.style.top = '0px';
        quote_el.style.display = 'block';
        let rect = element.getBoundingClientRect();
        let quote_rect = quote_el.getBoundingClientRect();

        let left_px = rect.left  + 18;
        let top_px = rect.top + 18;

        // 判断是否大于屏幕宽度
        let client_width = window.innerWidth;
        let spend_width = quote_rect.width + left_px;
        if (spend_width >= client_width && quote_rect.width <= client_width){
          left_px = left_px - (spend_width - client_width)

        }
        let translate_style = 'translate(' + left_px.toString() + 'px, ' + top_px.toString() + 'px)';
        quote_el.style.transform = translate_style;

        if (this.contexts[_id]) {
          this.quote_title = this.contexts[_id].title;
          this.quote_content = this.contexts[_id].content;
          this.quote_url = this.contexts[_id].url;
        }
        
      }
    };
    document.addEventListener('click', this._docClickHandler);
    return this.$store.dispatch('getSearchResultStrem', 1);
  },
  beforeUnmount() {
    if (this._docClickHandler) {
      document.removeEventListener('click', this._docClickHandler);
      this._docClickHandler = null;
    }
  },
  methods: {
    next_page(){
      let pageno = this.pageno + 1;
      return this.$store.dispatch('getSearchResult', pageno);
    },
    prev_page(){
      let pageno = this.pageno - 1;
      if (pageno > 0) return this.$store.dispatch('getSearchResult', pageno);
    },
    stop_receive_answer(){
      return this.$store.dispatch('stopReceiveAnswer');
    }
  },
  computed: {
    ...mapGetters({
      items: 'stateResults',
      contexts: 'stateContexts',
      question: 'searchQuestion',
      pageno: 'searchPageno',
      search_result_show: 'searchResultShow',
      ai_answer_show: 'aiAnswerShow',
      more_question_show: 'moreQuestionShow',
      ai_answer: 'aiAnswer',
      more_question: 'moreQuestion',
      stop_receive_answer_tag: 'stopReceiveAnswer',
    }),
  }
}
</script>
