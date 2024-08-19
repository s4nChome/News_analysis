<template>
  <el-form 
    ref="loginForm" 
    :model="loginForm" 
    @submit.native.prevent="login" 
    @keydown.enter.native="login"
    class="login-form">
    <h1>登录</h1>
    <el-form-item label="用户名" prop="username" :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]">
      <el-input v-model="loginForm.username" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item label="密码" prop="password" :rules="[{ required: true, message: '请输入密码', trigger: 'blur' }]">
      <el-input type="password" v-model="loginForm.password" autocomplete="off"></el-input>
    </el-form-item>
    <el-form-item>
      <div style="display: flex; justify-content: center;">
        <el-button type="danger" @click="clear">清空</el-button>
        <el-button type="success" @click="login">登录</el-button>
      </div>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data() {
    return {
      loginForm: {
        username: '',
        password: ''
      }
    };
  },
  methods: {
    clear() {
      this.$refs.loginForm.resetFields();
    },
    login() {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          if (this.loginForm.username === 'admin' && this.loginForm.password === '123456') {
              this.$notify({
                message: '登录成功',
                type: 'success'
              });
              this.$router.push({ path: '/mutil' });
          } else {
              this.$notify.error({
                  title: '错误',
                  message: '用户名或密码错误'
              });
          }
        } else {
          console.log('Error submit!!');
          return false;
        }
      });
    }
  }
};
</script>

<style scoped>
.login-form {
    width: 400px;
    padding: 25px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

h1 {
    text-align: center;
    color: #20a0ff;
}

el-button {
    width: 100%;
}

el-form-item {
    margin-bottom: 20px;
}
</style>
