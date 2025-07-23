// 通用API请求配置，基于axios
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // 本机后端接口地址
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器（如需token可在此加）
api.interceptors.request.use(config => {
  // const token = localStorage.getItem('token');
  // if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
}, err => Promise.reject(err));

// 响应拦截器（可统一处理错误）
api.interceptors.response.use(
  res => res.data,
  err => {
    // 可全局弹窗提示
    return Promise.reject(err);
  }
);

export default api;
