import { ElMessage, ElMessageBox } from 'element-plus'

export interface ApiError {
  message: string
  status?: number
  code?: string
}

export const handleApiError = (error: any, customMessage?: string) => {
  console.error('API Error:', error)
  
  let message = customMessage || '操作失败'
  let title = '错误'
  
  if (error?.response?.data?.detail) {
    message = error.response.data.detail
  } else if (error?.message) {
    message = error.message
  }
  
  // Handle specific error codes
  if (error?.response?.status) {
    switch (error.response.status) {
      case 401:
        title = '认证失败'
        message = '请重新登录'
        // Redirect to login page
        setTimeout(() => {
          window.location.href = '/login'
        }, 1000)
        break
      case 403:
        title = '权限不足'
        message = '您没有执行此操作的权限'
        break
      case 404:
        title = '资源不存在'
        message = '请求的资源未找到'
        break
      case 422:
        title = '数据验证失败'
        if (error.response.data?.detail?.[0]?.msg) {
          message = error.response.data.detail[0].msg
        }
        break
      case 500:
        title = '服务器错误'
        message = '服务器内部错误，请稍后重试'
        break
      case 503:
        title = '服务不可用'
        message = '服务暂时不可用，请稍后重试'
        break
    }
  }
  
  ElMessage({
    type: 'error',
    message: message,
    duration: 5000
  })
  
  return { title, message, status: error?.response?.status }
}

export const handleSuccess = (message: string = '操作成功', duration: number = 3000) => {
  ElMessage({
    type: 'success',
    message,
    duration
  })
}

export const confirmAction = async (
  message: string,
  title: string = '确认操作',
  type: 'warning' | 'info' | 'success' | 'error' = 'warning'
): Promise<boolean> => {
  try {
    await ElMessageBox.confirm(message, title, {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type
    })
    return true
  } catch {
    return false
  }
}