import{r as e,c as a,o as t,i as l,a as n,n as u,b as r,d as o,e as s,w as p,f as i,u as d,g as c,h as f,j as m,k as v}from"./vendor.20a6bbac.js";const h=c("大航海時代Online 非官方 商館店鋪檢索器 by 護衛艦-良良"),g=c(" 📑 使用說明： "),w=i("br",null,null,-1),b=c("1. 非即時資料，此工具大概會在半夜三點（+8時區）自動更新資料 "),_=i("br",null,null,-1),N=c("2. 商品關鍵字支援簡體轉繁體中文搜尋 "),y=i("br",null,null,-1),k=c("3. 有 bug 可以"),x=i("a",{href:"https://github.com/ALiangLiang/gvo-web-stores/issues"},"開 issue",-1),P=c(" 回報 "),A=i("br",null,null,-1),U=c("4. 如果有興趣增添功能、修 bug 也歡迎 PR "),j=c(" ☕ Donate 贊助： "),C=c(" 如果喜歡的話，也歡迎贊助支持，不然我也是得每個月課金才能用 @web 爬資料，也是有點成本呢，感謝各位~ "),O=c(" 台灣 Pay （110年底前免手續費） "),z=c(" 街口支付 "),V=c(" 如果有其他問題，可以至"),q=i("a",{href:"https://forum.gamer.com.tw/C.php?bsn=7200&snA=61970&tnum=1"},"巴哈討論串",-1),F=c("下留言 ");m({setup(c){const m=e([]),v=e(1),L=e(10),T=e(""),$=e([]),B=e([]),D=a((()=>B.value.map((e=>({text:e,value:e}))))),I=e([]),R=e([]),S=a((()=>R.value.map((e=>({text:e,value:e}))))),E=e(null);async function G({companies:e,serverName:a,townName:t,updatedAt:l}){const n=[];for(const u of e)for(const e of u.products)n.push({updatedAt:l,serverName:a,townName:t,companyName:u.company_name,productName:e.name,productAmount:e.amount,productUnitPrice:e.unit_price});return n}t((async function(){const e=l.service(),{data:a}=await n.get("data/stats.json");let t=[];B.value=[],R.value=[];for(const l in a){B.value.push(l);const e=a[l];for(const a in e){-1===R.value.indexOf(a)&&R.value.push(a);if(0===e[a])continue;const{data:u}=await n.get(`data/${l}-${a}.json`),{companies:r,updated_at:o}=u;t=t.concat(await G({companies:r,serverName:l,townName:a,updatedAt:o}))}}m.value=t,$.value=B.value,I.value=R.value,u((()=>e.close()))}));const H=a((function(){const e=f.exports.tify(T.value);return m.value.filter((a=>{const t=a.productName.match(e),l=f.exports.sify(a.productName).match(T.value);return!(""!==T.value&&!t&&!l)&&(-1!==$.value.indexOf(a.serverName)&&-1!==I.value.indexOf(a.townName))})).sort(((e,a)=>"ascending"===E.value?e.productUnitPrice-a.productUnitPrice:"descending"===E.value?a.productUnitPrice-e.productUnitPrice:0))})),J=a((function(){return H.value.slice((v.value-1)*L.value,v.value*L.value)}));function K(e,a,t,l){return(new Intl.NumberFormat).format(Number(t))}function M(e){v.value=e}function Q({column:e,prop:a,order:t}){"productUnitPrice"===a&&(E.value=t)}function W(e){e.serverName&&($.value=e.serverName),e.townName&&(I.value=e.townName)}function X(){return!0}return(e,a)=>{const t=r("el-header"),l=r("el-input"),n=r("el-table-column"),u=r("el-table"),c=r("el-pagination"),f=r("el-main"),m=r("el-col"),v=r("el-row"),B=r("el-link"),R=r("el-image"),E=r("el-footer"),G=r("el-container");return o(),s(G,null,{default:p((()=>[i(t,null,{default:p((()=>[h])),_:1}),i(f,null,{default:p((()=>[i(l,{modelValue:T.value,"onUpdate:modelValue":a[1]||(a[1]=e=>T.value=e),size:"mini",placeholder:"商品關鍵字"},null,8,["modelValue"]),i(u,{"row-key":"date",data:d(J),style:{width:"100%"},onSortChange:Q,onFilterChange:W},{default:p((()=>[i(n,{prop:"updatedAt",label:"更新日期",width:"180","column-key":"date"}),i(n,{prop:"serverName",label:"伺服器",width:"180","column-key":"serverName",filters:d(D),"filter-method":X,"filtered-value":$.value},null,8,["filters","filtered-value"]),i(n,{prop:"townName",label:"港口","column-key":"townName",filters:d(S),"filter-method":X,"filtered-value":I.value},null,8,["filters","filtered-value"]),i(n,{prop:"companyName",label:"商會"}),i(n,{prop:"productName",label:"商品"}),i(n,{prop:"productAmount",label:"數量"}),i(n,{prop:"productUnitPrice",sortable:"",label:"價格",formatter:K})])),_:1},8,["data"]),i(c,{background:"",layout:"prev, pager, next",total:d(H).length,"page-size":L.value.value,onCurrentChange:M},null,8,["total","page-size"])])),_:1}),i(E,null,{default:p((()=>[i(v,null,{default:p((()=>[i(m,{span:12},{default:p((()=>[g,w,b,_,N,y,k,x,P,A,U])),_:1}),i(m,{span:12},{default:p((()=>[i(v,null,{default:p((()=>[i(m,{span:24},{default:p((()=>[j])),_:1})])),_:1}),i(v,null,{default:p((()=>[i(m,{span:24},{default:p((()=>[C])),_:1})])),_:1}),i(v,null,{default:p((()=>[i(m,{span:12},{default:p((()=>[i(B,{type:"warning",href:"https://merchant.twmp.com.tw:20443/addongw/p2p/getByToken?token=6f8139fa-4f91-4956-aad9-0c730c483394",target:"_blank"},{default:p((()=>[O])),_:1})])),_:1}),i(m,{span:12},{default:p((()=>[i(B,{type:"warning",href:"https://www.jkopay.com/transfer?j=Transfer:900923228",target:"_blank"},{default:p((()=>[z])),_:1})])),_:1})])),_:1}),i(v,null,{default:p((()=>[i(m,{span:12},{default:p((()=>[i(R,{style:{width:"200px",height:"200px"},src:"assets/twpay-qrcode.png",fit:"fit"})])),_:1}),i(m,{span:12},{default:p((()=>[i(R,{style:{width:"200px",height:"200px"},src:"assets/jkpay-qrcode.png",fit:"fit"})])),_:1})])),_:1}),i(v,null,{default:p((()=>[i(m,{span:24},{default:p((()=>[V,q,F])),_:1})])),_:1})])),_:1})])),_:1})])),_:1})])),_:1})}}}).use(v).mount("#app");
