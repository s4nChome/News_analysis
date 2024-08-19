<template>
  <el-container>
    <el-header>
      <img src="@/assets/logo.png" alt="" style="width: 40px; position: relative; top: 10px;">
      <span style="font-size: 30px; margin-left: 5px;">军事新闻抽取系统</span>
    </el-header>

    <el-main>
      <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 2 }" placeholder="请输入要批量爬取的链接" v-model="input_text" style="width: 60%; margin-top: 5px;"></el-input>
      <div style="padding-top: 20px;">
        <el-button type="warning" @click="clearAll">清空内容</el-button>
        <el-button type="success" @click="getUrls">爬取URL</el-button>
        <el-button type="primary" @click="getSwitch">切换单个爬取</el-button>
      </div>

      <div>
        <el-table v-loading="loading1" :data="tableData" stripe style="width: 100%;margin-top: 40px; ">
          <el-table-column label="新闻网址">
          <template slot-scope="scope">
            <el-link type="primary" :href="scope.row.url" target="_blank">{{ scope.row.url }}</el-link>
          </template>
        </el-table-column>
          <el-table-column prop="title" label="标题"></el-table-column>
          <el-table-column prop="" label="操作" >
            <template slot-scope="scope">
              <el-button type="primary" @click="handleSelect(scope.row.url)">选择</el-button>
            </template>
          </el-table-column>  
        </el-table>
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
      input_text: '',
      tableData: [],
      loading1: false,
    }
  },

  methods: {

    getUrls() {
      this.tableData = [];
      this.loading1 = true;
      axios.post('http://127.0.0.1:5000/api/getUrls', {
        data: this.input_text
      })
      .then((response) => {
        this.tableData = response.data.data;
      })
      .catch((error) => {
        console.log(error);
      })
      .finally(() => {
        this.loading1 = false;
      });
    },

    getSwitch() {
      this.$router.push({ path: '/single' });
    },

    handleSelect(url) {
      this.$router.push({ path: '/single', query: { url: url } });
    },

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