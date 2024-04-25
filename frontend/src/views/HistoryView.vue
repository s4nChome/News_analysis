<template>
  
  <el-container>
    <el-header>
      <img src="@/assets/logo.png" alt="" style="width: 40px; position: relative; top: 10px;">
      <span style="font-size: 30px; margin-left: 5px;">军事新闻抽取系统</span>
    </el-header>

    <el-main style="width: 100%;">
      <el-button type="text" style="float: left" @click="returnHome">返回主页</el-button>
      <el-table :data="tableData" stripe style="width: 100%;margin-top: 40px;">
        <el-table-column prop="id" label="ID" show-overflow-tooltip></el-table-column>
        <el-table-column prop="time" label="时间" show-overflow-tooltip></el-table-column>
        <el-table-column label="新闻网址" show-overflow-tooltip>
          <template slot-scope="scope">
            <el-link v-if="scope.row.url" type="primary" :href="scope.row.url" target="_blank">{{ scope.row.url }}</el-link>
            <span v-else>无</span>
          </template>
        </el-table-column>

        <el-table-column label="网址可信度" show-overflow-tooltip>
          <template slot-scope="scope">
            <!-- 可信 -->
            <el-tag v-if="['trusted','credible'].includes(scope.row.domain_category)" type="success">可信</el-tag>
            <!-- 未知 -->
            <el-tag v-else-if="['unknown','unsure'].includes(scope.row.domain_category)" type="primary">未知</el-tag>
            <!-- 不可信 -->
            <el-tag v-else-if="['fake', 'unreliable', 'bias', 'clickbait', 'conspiracy', 'hate', 'junksci', 'rumor'].includes(scope.row.domain_category)" type="danger">不可信</el-tag>
            <!-- 可疑 -->
            <el-tag v-else-if="['satire', 'parody', 'political', 'state'].includes(scope.row.domain_category)" type="warning">可疑</el-tag>
            <!-- 默认无 -->
            <el-tag v-else type="info">无</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="标题可信度" show-overflow-tooltip>
          <template slot-scope="scope">
            <el-progress :percentage="Math.floor(scope.row.title_score * 100)" :color="getProgressColor"></el-progress>
          </template>
        </el-table-column>
        
        <el-table-column label="内容可信度" show-overflow-tooltip>
          <template slot-scope="scope">
            <el-progress :percentage="Math.floor(scope.row.content_score * 100)" :color="getProgressColor"></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="key_words" label="关键词" show-overflow-tooltip></el-table-column>
        <el-table-column label="新闻标题" show-overflow-tooltip>
          <template slot-scope="scope">
            {{ scope.row.title ? scope.row.title : '无' }}
          </template>
        </el-table-column>
        <el-table-column prop="content" label="新闻内容" show-overflow-tooltip></el-table-column>
        <el-table-column prop="analysis_result" label="分析结果" show-overflow-tooltip>
          <template slot-scope="scope">
            {{ scope.row.analysis_result ? scope.row.analysis_result : '未进行分析' }}
          </template>

        </el-table-column>
      </el-table>



      <div style="margin-top: 20px;">
      <el-pagination
        :page-size="params.pageSize"
        :current-page="params.pageNum"
        layout="prev, pager, next"
        @current-change="handleCurrentChange"
        :total="total">
      </el-pagination>
    </div>


    </el-main>
  </el-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tableData: [],
      total: 0,
      params: {
        pageNum: 1,
        pageSize: 12,
      }
    };
  },

  created() {
    this.load();
  },

  methods: {
    load() {
      axios.get('http://127.0.0.1:5000/api/history', {
          params: this.params
        })
        .then((res) => {
          this.tableData = res.data.data.list;
          this.total = res.data.data.total;
          this.$notify({
            message: '获取历史记录成功',
            type: 'success'
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },

    handleCurrentChange(pageNum) {
      this.params.pageNum = pageNum
      this.load()
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

    returnHome() {
      this.$router.push({ path: '/' });
    }
  },
}
</script>
