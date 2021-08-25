<template>
  <el-container>
    <el-header>大航海時代Online 非官方 商館店鋪檢索器 by 護衛艦-良良</el-header>
    <el-main>
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
    </el-main>
    <el-footer>
      <el-row>
        <el-col :span="12">
          📑 使用說明：
          <br>1. 非即時資料，此工具大概會在半夜三點（+8時區）自動更新資料
          <br>2. 商品關鍵字支援簡體轉繁體中文搜尋
          <br>3. 有 bug 可以<a href="https://github.com/ALiangLiang/gvo-web-stores/issues">開 issue</a> 回報
          <br>4. 如果有興趣增添功能、修 bug 也歡迎 PR
        </el-col>
        <el-col :span="12">
          <el-row>
            <el-col :span="24">
              ☕ Donate 贊助：
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              如果喜歡的話，也歡迎贊助支持，不然我也是得每個月課金才能用 @web 爬資料，也是有點成本呢，感謝各位~
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-link
                type="warning"
                href="https://merchant.twmp.com.tw:20443/addongw/p2p/getByToken?token=6f8139fa-4f91-4956-aad9-0c730c483394"
                target="_blank"
              >
                台灣 Pay （110年底前免手續費）
              </el-link>
            </el-col>
            <el-col :span="12">
              <el-link
                type="warning"
                href="https://www.jkopay.com/transfer?j=Transfer:900923228"
                target="_blank"
              >
                街口支付
              </el-link>
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="12">
              <el-image
                style="width: 200px; height: 200px"
                src="assets/twpay-qrcode.png"
                fit="fit"
              />
            </el-col>
            <el-col :span="12">
              <el-image
                style="width: 200px; height: 200px"
                src="assets/jkpay-qrcode.png"
                fit="fit"
              />
            </el-col>
          </el-row>
          <el-row>
            <el-col :span="24">
              如果有其他問題，可以至<a href="https://forum.gamer.com.tw/C.php?bsn=7200&snA=61970&tnum=1">巴哈討論串</a>下留言
            </el-col>
          </el-row>
        </el-col>
      </el-row>
    </el-footer>
  </el-container>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted, computed, nextTick } from 'vue'
import { ElLoading } from 'element-plus'
import { tify, sify } from 'chinese-conv'

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

  nextTick(() => loadingInstance.close())
})

const tableData = computed(function () {
  const traditionalChineseSearch = tify(search.value)
  const filtered = productsData.value.filter((row) => {
    // Filtered by search
    const tMatchS = row.productName.match(traditionalChineseSearch)
    const sMatchT = sify(row.productName).match(search.value)
    if (search.value !== '' && !(tMatchS || sMatchT)) {
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
  currentPage.value = page
}

function onChangeSort ({ column, prop, order }) {
  if (prop === 'productUnitPrice') {
    priceOrder.value = order
  }
}

function onChangeFilter (filters) {
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
