import axios from 'axios';
import { EventSourcePolyfill } from "event-source-polyfill";

const state = {
  search_results: [],
  contexts: [],
  search_question: '',
  more_question: [],
  more_question_str: '',
  ai_answer: '',
  search_pageno: 1,
  search_result_show: 0,
  ai_answer_show: 0,
  more_question_show: 0,
  stop_receive_answer: 0,
  eventSource: null,
};

const getters = {
  stateResults: state => state.search_results,
  stateContexts: state => state.contexts,
  searchQuestion: state => state.search_question,
  aiAnswer: state => state.ai_answer,
  moreQuestion: state => state.more_question,
  searchPageno: state => state.search_pageno,
  searchResultShow: state => state.search_result_show,
  aiAnswerShow: state => state.ai_answer_show,
  moreQuestionShow: state => state.more_question_show,
  stopReceiveAnswer: state => state.stop_receive_answer,
};

const actions = {
  async stopReceiveAnswer({commit}) {
    await commit('setStopReceive', 1);
    if (state.eventSource) {
      state.eventSource.close();
      state.eventSource = null;
    }
  },
  async getSearchResultStrem({commit}, pageno) {
    let urlParams = new URLSearchParams(window.location.search);
    let question = urlParams.get('question');
    await commit('setQuestion', question);
    await commit('setHide', true);
    await commit('setStopReceive', 0);
    state.more_question_str = '';
    state.ai_answer = '';

    if (!pageno) {
      pageno = 1;
    }
    await commit('setPageno', pageno);
    let params = 'q=' + question + '&pageno=' + pageno;
    let url = import.meta.env.VITE_APP_BASE_API + '/search/query';

    state.eventSource = new EventSourcePolyfill(`${url}?${params}`, {});
    state.eventSource.addEventListener('more_question', event => {
      commit('setMoreQuestion', event.data);
    });
    state.eventSource.addEventListener('search_results', event => {
      commit('setSearchResults', JSON.parse(event.data));
    });
    state.eventSource.addEventListener('contexts', event => {
      commit('setContexts', JSON.parse(event.data));
    });
    state.eventSource.addEventListener('answer', event => {
      commit('setAiAnswer', event.data);
    });
    state.eventSource.addEventListener('end_answer', event => {
      commit('setStopReceive', 1);
    });
    // 监听error
    state.eventSource.addEventListener('error', event => {
      if (event.type === 'error') {
        console.error('Connection error:', event.message);
      } else if (event.type === 'exception') {
        console.error('Error:', event.message, event.error);
      }
      if (state.eventSource) {
        state.eventSource.close();
      }
    });
    // 监听close
    state.eventSource.addEventListener('close', event => {
      console.log('Close SSE connection.');
    });
  },
  async getSearchResult({commit}, pageno) {
    let urlParams = new URLSearchParams(window.location.search);
    let question = urlParams.get('question');
    await commit('setQuestion', question);
    await commit('setHide');

    if (!pageno) {
      pageno = 1;
    }
    await commit('setPageno', pageno);
    //let params = {keyword: `${keyword}`, type: `${type}`}
    let params = {q: `${question}`, pageno: `${pageno}`}

    let {data} = await axios.post('/search/search_query', params);
    await commit('setSearchResults', data.data);
  }
};

const mutations = {
  setSearchResults(state, data) {
    state.search_results = data;
    state.search_result_show = 1;
  },
  setContexts(state, data) {
    state.contexts = data;
  },
  setAiAnswer(state, data) {
    if (!state.stop_receive_answer){
      state.ai_answer = state.ai_answer + data;
      state.ai_answer = state.ai_answer
      .replace(/\[\[([cC])itation/g, "[citation")
      .replace(/[cC]itation:(\d+)]]/g, "citation:$1]")
      .replace(/\[\[([cC]itation:\d+)]](?!])/g, `[$1]`)
      .replace(/\[[cC]itation:(\d+)]/g, "[citation]($1)")
      .replace(/\[\[citation:(\d+)\]\]/g, "[citation]($1)")
      .replace(/\[citation\]\((\d+)\)/g, '<span id="quote_$1" quote_id="$1" name="quote_number" class="quote inline-block size-4 cursor-pointer text-xs font-medium bg-slate-100 text-slate-500 dark:bg-slate-700 dark:text-slate-100 rounded-full text-center px-1.5 ml-1 hover:opacity-80">$1</span>'),
      //console.log(data)
      state.ai_answer_show = 1;
    }
  },
  setMoreQuestion(state, data){
    state.more_question_str = state.more_question_str + data;
    state.more_question = state.more_question_str.split('\n');
    state.more_question_show = 1;
  },
  setStopReceive(state, data){
    state.stop_receive_answer = data;
  },
  setHide(state, hide_ai_answer=false) {
    state.search_result_show = 0;
    if(hide_ai_answer){
      state.ai_answer_show = 0;
      state.more_question_show = 0;
    }
  },
  setQuestion(state, data) {
    state.search_question = data;
  },
  setPageno(state, data) {
    state.search_pageno = data;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
