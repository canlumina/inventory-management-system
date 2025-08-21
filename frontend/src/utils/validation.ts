import type { FormItemRule } from 'element-plus'

// Common validation rules
export const validationRules = {
  required: (message = '此项为必填项'): FormItemRule => ({
    required: true,
    message,
    trigger: 'blur'
  }),

  email: (message = '请输入正确的邮箱格式'): FormItemRule => ({
    type: 'email',
    message,
    trigger: 'blur'
  }),

  phone: (message = '请输入正确的手机号码'): FormItemRule => ({
    pattern: /^1[3-9]\d{9}$/,
    message,
    trigger: 'blur'
  }),

  minLength: (min: number, message?: string): FormItemRule => ({
    min,
    message: message || `至少输入${min}个字符`,
    trigger: 'blur'
  }),

  maxLength: (max: number, message?: string): FormItemRule => ({
    max,
    message: message || `最多输入${max}个字符`,
    trigger: 'blur'
  }),

  range: (min: number, max: number, message?: string): FormItemRule => ({
    min,
    max,
    message: message || `长度在${min}到${max}个字符`,
    trigger: 'blur'
  }),

  number: (message = '请输入数字'): FormItemRule => ({
    type: 'number',
    message,
    trigger: 'blur'
  }),

  integer: (message = '请输入整数'): FormItemRule => ({
    pattern: /^-?\d+$/,
    message,
    trigger: 'blur'
  }),

  positiveNumber: (message = '请输入正数'): FormItemRule => ({
    validator: (_rule: any, value: any, callback: Function) => {
      if (value !== undefined && value !== null && value !== '') {
        const num = Number(value)
        if (isNaN(num) || num <= 0) {
          callback(new Error(message))
        } else {
          callback()
        }
      } else {
        callback()
      }
    },
    trigger: 'blur'
  }),

  positiveInteger: (message = '请输入正整数'): FormItemRule => ({
    validator: (_rule: any, value: any, callback: Function) => {
      if (value !== undefined && value !== null && value !== '') {
        const num = Number(value)
        if (isNaN(num) || num <= 0 || !Number.isInteger(num)) {
          callback(new Error(message))
        } else {
          callback()
        }
      } else {
        callback()
      }
    },
    trigger: 'blur'
  }),

  decimal: (precision: number = 2, message?: string): FormItemRule => ({
    validator: (_rule: any, value: any, callback: Function) => {
      if (value !== undefined && value !== null && value !== '') {
        const num = Number(value)
        if (isNaN(num)) {
          callback(new Error(message || '请输入有效数字'))
        } else {
          const decimal = value.toString().split('.')[1]
          if (decimal && decimal.length > precision) {
            callback(new Error(message || `小数位数不能超过${precision}位`))
          } else {
            callback()
          }
        }
      } else {
        callback()
      }
    },
    trigger: 'blur'
  }),

  url: (message = '请输入正确的网址'): FormItemRule => ({
    type: 'url',
    message,
    trigger: 'blur'
  }),

  date: (message = '请选择日期'): FormItemRule => ({
    type: 'date',
    message,
    trigger: 'change'
  }),

  array: (message = '请至少选择一项'): FormItemRule => ({
    type: 'array',
    min: 1,
    message,
    trigger: 'change'
  }),

  custom: (validator: Function, message?: string): FormItemRule => ({
    validator: (_rule: any, value: any, callback: Function) => {
      try {
        const result = validator(value)
        if (result === true) {
          callback()
        } else {
          callback(new Error(message || result || '验证失败'))
        }
      } catch (error) {
        callback(new Error(message || '验证过程中发生错误'))
      }
    },
    trigger: 'blur'
  })
}

// Form validation helpers
export const createRules = (rulesConfig: Record<string, (FormItemRule | FormItemRule[])[]>) => {
  const rules: Record<string, FormItemRule[]> = {}
  
  for (const [field, fieldRules] of Object.entries(rulesConfig)) {
    rules[field] = fieldRules.flat()
  }
  
  return rules
}

// Common form rule combinations
export const commonRules = {
  username: [
    validationRules.required('请输入用户名'),
    validationRules.range(3, 20, '用户名长度在3到20个字符')
  ],
  
  password: [
    validationRules.required('请输入密码'),
    validationRules.minLength(6, '密码至少6个字符')
  ],
  
  email: [
    validationRules.required('请输入邮箱'),
    validationRules.email()
  ],
  
  phone: [
    validationRules.required('请输入手机号'),
    validationRules.phone()
  ],
  
  name: [
    validationRules.required('请输入名称'),
    validationRules.range(1, 50)
  ],
  
  code: [
    validationRules.required('请输入编码'),
    validationRules.range(1, 20)
  ],
  
  price: [
    validationRules.required('请输入价格'),
    validationRules.positiveNumber('请输入有效的价格'),
    validationRules.decimal(2, '价格最多保留2位小数')
  ],
  
  quantity: [
    validationRules.required('请输入数量'),
    validationRules.positiveInteger('请输入有效的数量')
  ],
  
  description: [
    validationRules.maxLength(500, '描述最多500个字符')
  ]
}

export default validationRules