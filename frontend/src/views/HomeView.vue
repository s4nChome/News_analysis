<template>
  <el-container>
    <el-header>
      <img src="@/assets/logo.png" alt="" style="width: 40px; position: relative; top: 10px;">
      <span style="font-size: 30px; margin-left: 5px;">军事新闻抽取系统</span>
    </el-header>

    <el-main>
      <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 2 }" placeholder="请输入新闻链接或新闻内容" v-model="input_text" style="width: 60%; margin-top: 5px;"></el-input>
      <div style="padding-top: 20px;">
        <el-button type="warning" @click="clearAll">清空内容</el-button>
        <el-button type="success" @click="getResult">获取新闻</el-button>
        <el-button type="primary" @click="getAnalysis">分析新闻</el-button>
      </div>
      <div>
        <el-descriptions v-loading="loading1" class="margin-top" title="新闻信息" :column="2" :size="size" border>
          <el-descriptions-item label="新闻网址">
            <el-link :href="url" target="_blank">{{ url }}</el-link>
          </el-descriptions-item>
          <el-descriptions-item label="网址可信度">
            <template v-if="['trusted','credible'].includes(domain_category)">
              <el-tag type="success">可信</el-tag>
            </template>
            <template v-else-if="['unknown','unsure'].includes(domain_category)">
              <el-tag type="primary">未知</el-tag>
            </template>
            <template v-else-if="['fake', 'unreliable', 'bias', 'clickbait', 'conspiracy', 'hate', 'junksci', 'rumor'].includes(domain_category)">
              <el-tag type="danger">不可信</el-tag>
            </template>
            <template v-else-if="['satire', 'parody', 'political', 'state'].includes(domain_category)">
              <el-tag type="warning">可疑</el-tag>
            </template>
            <template v-else>
              <el-tag type="info">无</el-tag>
            </template>
          </el-descriptions-item>
          <el-descriptions-item label="标题可信度">
            <el-progress :percentage="Math.floor(title_score * 100)" :color="getProgressColor"></el-progress>
          </el-descriptions-item>
          <el-descriptions-item label="内容可信度">
            <el-progress :percentage="Math.floor(content_score * 100)" :color="getProgressColor"></el-progress>
          </el-descriptions-item>
          <el-descriptions-item label="关键词">
            <div style="min-height: 1.5em; max-height: 1.5em; overflow-y: auto; line-height: 1.5em;">{{ key_words }}</div>
          </el-descriptions-item>
          <el-descriptions-item label="新闻标题">
            <div style="min-height: 1.5em; max-height: 1.5em; overflow-y: auto; line-height: 1.5em;">{{ title }}</div>
          </el-descriptions-item>
          <el-descriptions-item label="新闻内容">
            <div style="min-height: 9em; max-height: 9em; overflow-y: auto; line-height: 1.5em;">{{ content }}</div>
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <el-descriptions v-loading="loading2" class="margin-top" title="分析结果" :column="1" :size="size" border style="margin-top: 30px;">
        <el-descriptions-item label="内容分析">
          <div style="min-height: 16.5em; max-height: 16.5em; overflow-y: auto; line-height: 1.5em;">{{ content_analysis }}</div>
        </el-descriptions-item>
      </el-descriptions>
      <div style="margin-top: 10px;float: right;">
        <el-button type="primary" size="default" @click="getHistory">查看历史</el-button>
        <el-button type="primary" size="default" @click="getAnalysisAgain">重新分析</el-button>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomeView',

  data() {
    return {
      size: null,
      input_text: '',
      id: '',
      url: '',
      domain_category: '',
      key_words: '',
      title: '',
      title_decision: '',
      title_score: '',
      content: '',
      content_decision: '',
      content_score: '',
      content_analysis: '',
      loading1: false,
      loading2: false,
    }
  },

  methods: {
    clearAll() {
      this.input_text = '';
      this.url = '';
      this.domain_category = '';
      this.key_words = '';
      this.title = '';
      this.title_decision = '';
      this.title_score = '';
      this.content = '';
      this.content_decision = '';
      this.content_score = '';
      this.content_analysis = '';
    },

    getResult() {
      if (this.input_text === '') {
        this.$notify.error('请输入新闻链接或新闻内容');
        return;
      } else {
        this.loading1 = true;
        axios.post('http://127.0.0.1:5000/api/getResult', {
          data: this.input_text
        }).then(res => {
          this.id = res.data.data.id;
          this.url = res.data.data.url || "无";
          this.domain_category = res.data.data.domain_category || "无";
          this.key_words = res.data.data.key_words;
          this.title = res.data.data.title || "无";
          this.title_decision = res.data.data.title_decision;
          this.title_score = res.data.data.title_score;
          this.content = res.data.data.content;
          this.content_decision = res.data.data.content_decision;
          this.content_score = res.data.data.content_score;
          this.$notify.success(res.data.message);
        }).catch(err => {
          this.$notify.error(err);
        }).finally(() => {
          this.loading1 = false;
        });
      }
    },

    getProgressColor(percentage) {
      if (percentage < 30) {
        return '#f56c6c';
      } else if (percentage < 70) {
        return '#e6a23c';
      } else {
        return '#67c23a';
      }
    },

    getAnalysis() {
      if (this.content === "") {
        this.$notify.error('请先获取新闻信息');
        return;
      } else {
        this.loading2 = true;
        axios.post('http://127.0.0.1:5000/api/analysis', {
          id: this.id,
          data: this.title !== "无" ? this.title : this.content
        }).then(res => {
          this.content_analysis = res.data.data;
          this.$notify.success(res.data.message);
        }).catch(err => {
          this.$notify.error(err);
        }).finally(() => {
          this.loading2 = false;
        });
      }
    },

    getAnalysisAgain() {
      this.content_analysis = '';
      this.getAnalysis();
    },

    getHistory() {
      this.$router.push({ path: '/history' });
    }
  }
}
</script>

<style>
.el-header {
  background-color: white;
  text-align: center;
  line-height: 60px;
}

.el-main {
  width: 80%;
  min-height: calc(100vh - 65px);
  margin: 0 auto;
  margin-top: 5px;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: white;
  border-radius: 5px;
  text-align: center;
}

.el-descriptions-item__label {
  width: 6.5%;
}
</style>
