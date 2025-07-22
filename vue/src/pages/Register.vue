<template>
  <div class="register-container">
    <div class="form-card">
      <h2>创建账号</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名</label>
          <input
            type="text"
            v-model="username"
            placeholder="请输入用户名"
            required
          >
        </div>
        <div class="form-group">
          <label>密码</label>
          <input
            type="password"
            v-model="password"
            placeholder="请输入密码"
            required
          >
        </div>
        <div class="form-group">
          <label>用户类型</label>
          <div class="type-selector">
            <label
              v-for="type in userTypes"
              :key="type"
              :class="{ active: userType === type }"
            >
              <input
                type="radio"
                v-model="userType"
                :value="type"
                required
              >
              {{ type }}
            </label>
          </div>
        </div>
        <button type="submit" class="primary-btn">立即注册</button>
        <div class="form-tip">
          已有账号？<router-link to="/login">立即登录</router-link>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "@/utils/api.js"
export default {
  data() {
    return {
      username: '',
      password: '',
      userType: '听众',
      userTypes: ['听众', '演讲者']
    }
  },
  methods: {
    async handleRegister() {
      try {
        const params = new URLSearchParams();
        params.append('username', this.username);
        params.append('password', this.password);
        params.append('user_type', this.userType); // 修正参数名为 user_type
        const res = await axios.post('/sign', params, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        });
        if (res.res) { // 直接用 res.res
          this.$message?.success('注册成功，请登录')
          this.$router.push('/login')
        } else {
          this.$message?.error('注册失败，用户名已存在')
        }
      } catch (e) {
        this.$message?.error('注册失败，请重试')
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.form-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

h2 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

.type-selector {
  display: flex;
  gap: 1rem;
}

.type-selector label {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.type-selector input[type="radio"] {
  display: none;
}

.type-selector label.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.primary-btn {
  width: 100%;
  padding: 0.8rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.primary-btn:hover {
  background-color: #45a049;
}
.form-tip {
  margin-top: 1.2rem;
  text-align: center;
  color: #888;
  font-size: 0.98rem;
}
.form-tip a {
  color: #4CAF50;
  text-decoration: underline;
  margin-left: 4px;
}
</style>
