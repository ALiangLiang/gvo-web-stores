<template>
  <el-input
    v-model="search"
    size="mini"
    placeholder="商品關鍵字"
  />
  <el-table
    row-key="date"
    :data="pagedTableData"
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
      :filters="filteredServerNames"
      :filter-method="filterHandler"
      :filtered-value="selectedServers"
    />
    <el-table-column
      prop="townName"
      label="港口"
      column-key="townName"
      :filters="filteredTownNames"
      :filter-method="filterHandler"
      :filtered-value="selectedTowns"
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
    :page-size="pageSize.value"
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
const selectedServers = ref([])
const serverNames = ref([])
const filteredServerNames = computed(() =>
  serverNames.value.map((serverName) => ({
    text: serverName,
    value: serverName
  }))
)
const selectedTowns = ref([])
const townNames = ref([])
const filteredTownNames = computed(() =>
  townNames.value.map((townName) => ({
    text: townName,
    value: townName
  }))
)
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
  serverNames.value = []
  townNames.value = []
  for (const serverName in servers) {
    serverNames.value.push(serverName)

    const server = servers[serverName]
    for (const townName in server) {
      if (townNames.value.indexOf(townName) === -1) {
        townNames.value.push(townName)
      }

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

  selectedServers.value = serverNames.value
  selectedTowns.value = townNames.value
  console.log(selectedServers.value, selectedTowns.value)

  nextTick(() => loadingInstance.close())
})

const tableData = computed(function () {
  console.log(selectedServers, selectedServers.value)
  const filtered = productsData.value.filter((row) => {
    // Filtered by search
    if (search.value !== '' && !row.productName.match(search.value)) {
      return false
    }

    // Filtered by server name
    if (selectedServers.value.indexOf(row.serverName) === -1) {
      return false
    }

    // Filtered by town name
    if (selectedTowns.value.indexOf(row.townName) === -1) {
      return false
    }

    return true
  })
  console.log(filtered)

  // Sort by price
  return filtered.sort((a, b) => {
    if (priceOrder.value === 'ascending') {
      return a.productUnitPrice - b.productUnitPrice
    } else if (priceOrder.value === 'descending') {
      return b.productUnitPrice - a.productUnitPrice
    }
    return 0
  })
})

const pagedTableData = computed(function () {
  return tableData.value.slice(
    (currentPage.value - 1) * pageSize.value,
    currentPage.value * pageSize.value
  )
})

function formatPrice (row, column, cellValue, index) {
  const formatter = new Intl.NumberFormat()
  return formatter.format(Number(cellValue))
}

function onChangePage (page) {
  console.log('onChangePage', page)
  currentPage.value = page
}

function onChangeSort ({ column, prop, order }) {
  if (prop === 'productUnitPrice') {
    priceOrder.value = order
  }
}

function onChangeFilter (filters) {
  console.log(filters)
  if (filters.serverName) {
    selectedServers.value = filters.serverName
  }
  if (filters.townName) {
    selectedTowns.value = filters.townName
  }
}

function filterHandler () {
  return true
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
</style>
