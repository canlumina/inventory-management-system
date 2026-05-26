import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const viewsDir = fileURLToPath(new URL('../views', import.meta.url))

function collectVueFiles(dir) {
  const files = []

  for (const entry of readdirSync(dir)) {
    const path = join(dir, entry)
    const stat = statSync(path)

    if (stat.isDirectory()) {
      files.push(...collectVueFiles(path))
    } else if (path.endsWith('.vue')) {
      files.push(path)
    }
  }

  return files
}

test('view components do not contain console debugging calls', () => {
  const offenders = collectVueFiles(viewsDir)
    .filter((file) => /console\.\w+/.test(readFileSync(file, 'utf8')))
    .map((file) => file.replace(`${viewsDir}/`, ''))

  assert.deepEqual(offenders, [])
})

test('ReportsView does not ship placeholder mock ranking data', () => {
  const reportsView = readFileSync(new URL('../views/ReportsView.vue', import.meta.url), 'utf8')

  assert.equal(reportsView.includes('模拟数据'), false)
  assert.equal(reportsView.includes('iPhone 14 Pro'), false)
})

test('ProductsView refreshes category options when restored from keep-alive', () => {
  const appView = readFileSync(new URL('../App.vue', import.meta.url), 'utf8')
  const productsView = readFileSync(new URL('../views/ProductsView.vue', import.meta.url), 'utf8')

  assert.match(appView, /<keep-alive>/)
  assert.match(productsView, /import\s+\{[^}]*onActivated[^}]*\}\s+from\s+'vue'/)
  assert.match(productsView, /onActivated\(\s*\(\)\s*=>\s*\{[\s\S]*loadCategories\(\)/)
})
