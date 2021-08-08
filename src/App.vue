<template>
  <el-input
    v-model="search"
    size="mini"
    placeholder="商品關鍵字"
  />
  <el-table
    row-key="date"
    :data="
      filteredTableData.slice(
        (currentPage - 1) * pagesize,
        currentPage * pagesize
      )
    "
    style="width: 100%"
  >
    <el-table-column
      prop="updatedAt"
      label="更新日期"
      sortable
      width="180"
      column-key="date"
    />
    <el-table-column
      prop="serverName"
      label="伺服器"
      width="180"
      :filters="[
        { text: '護衛艦(推薦)', value: '護衛艦(推薦)' },
        { text: '探索號(推薦)', value: '探索號(推薦)' },
        { text: '幽靈船', value: '幽靈船' },
        { text: '戰列艦', value: '戰列艦' },
      ]"
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
      label="價格"
      :formatter="formatPrice"
    />
  </el-table>
  <el-pagination
    background
    layout="prev, pager, next"
    :total="filteredTableData.length"
    :page-size="pagesize"
    @current-change="onChangePage"
  />
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed } from 'vue'

const tableData = ref([])
const currentPage = ref(1)
const pagesize = ref(10)
const search = ref('')

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
  tableData.value = rows
})

const filteredTableData = computed(function () {
  return tableData.value.filter((row) => {
    if (search.value !== '') {
      return row.productName.match(search.value)
    }
    return true
  })
})

function formatPrice (row, column, cellValue, index) {
  const formatter = new Intl.NumberFormat()
  return formatter.format(Number(cellValue))
}

function onChangePage (page) {
  console.log(page)
  currentPage.value = page
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
