<template>
  <el-input
    v-model="search"
    size="mini"
    placeholder="商品關鍵字"
  />
  <el-table
    row-key="date"
    :data="tableData"
    style="width: 100%"
    @sort-change="onChangeSort"
    @filter-change="onChangeFilter"
  >
    <el-table-column
      prop="updatedAt"
      label="更新日期"
      width="180"
      column-key="date"
    />
    <el-table-column
      prop="serverName"
      label="伺服器"
      width="180"
      column-key="serverName"
      :filters="[
        { text: '護衛艦(推薦)', value: '護衛艦(推薦)' },
        { text: '探索號(推薦)', value: '探索號(推薦)' },
        { text: '幽靈船', value: '幽靈船' },
        { text: '戰列艦', value: '戰列艦' },
      ]"
      :filtered-value="filteredValue"
    />
    <el-table-column
      prop="townName"
      label="港口"
    />
    <el-table-column
      prop="companyName"
      label="商會"
    />
    <el-table-column
      prop="productName"
      label="商品"
    />
    <el-table-column
      prop="productAmount"
      label="數量"
    />
    <el-table-column
      prop="productUnitPrice"
      sortable
      label="價格"
      :formatter="formatPrice"
    />
  </el-table>
  <el-pagination
    background
    layout="prev, pager, next"
    :total="tableData.length"
    :page-size="pageSize"
    @current-change="onChangePage"
  />
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed, nextTick } from 'vue'
import { ElLoading } from 'element-plus'

const productsData = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const search = ref('')
const filteredValue = ref(['護衛艦(推薦)', '探索號(推薦)', '幽靈船', '戰列艦'])
const priceOrder = ref(null)

async function formatCompanies ({ companies, serverName, townName, updatedAt }) {
  const rows = []
  for (const company of companies) {
    for (const prod of company.products) {
      rows.push({
        updatedAt,
        serverName,
        townName,
        companyName: company.company_name,
        productName: prod.name,
        productAmount: prod.amount,
        productUnitPrice: prod.unit_price
      })
    }
  }
  return rows
}

onMounted(async function () {
  const loadingInstance = ElLoading.service()

  const { data: servers } = await axios.get('data/stats.json')
  let rows = []
  for (const serverName in servers) {
    const server = servers[serverName]
    for (const townName in server) {
      const totalProductsInTown = server[townName]
      if (totalProductsInTown === 0) {
        continue
      }

      const { data } = await axios.get(`data/${serverName}-${townName}.json`)
      const { companies, updated_at: updatedAt } = data
      rows = rows.concat(
        await formatCompanies({
          companies,
          serverName,
          townName,
          updatedAt
        })
      )
    }
  }
  productsData.value = rows

  nextTick(() => { // 以服务的方式调用的 Loading 需要异步关闭
    loadingInstance.close()
  })
})

const tableData = computed(function () {
  const filtered = productsData.value.filter((row) => {
    // Filtered by search
    if (search.value !== '' && !row.productName.match(search.value)) {
      console.log(search.value)
      return false
    }

    // Filtered by server name
    if (filteredValue.value.indexOf(row.serverName) === -1) {
      return false
    }

    return true
  })

  // Sort by price
  const sorted = filtered.sort((a, b) => {
    if (priceOrder.value === 'ascending') {
      return a.productUnitPrice - b.productUnitPrice
    } else if (priceOrder.value === 'descending') {
      return b.productUnitPrice - a.productUnitPrice
    }
    return 0
  })

  return sorted.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

function formatPrice (row, column, cellValue, index) {
  const formatter = new Intl.NumberFormat()
  return formatter.format(Number(cellValue))
}

function onChangePage (page) {
  currentPage.value = page
}

function onChangeSort ({ column, prop, order }) {
  if (prop === 'productUnitPrice') {
    priceOrder.value = order
  }
}

function onChangeFilter (filters) {
  filteredValue.value = filters.serverName
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.element-plus-logo {
  width: 50%;
}
</style>
