"use strict";(self["webpackChunkvue3_element_plus_demo_test"]=self["webpackChunkvue3_element_plus_demo_test"]||[]).push([[11],{7237:function(e,a,t){t.d(a,{A7:function(){return u},jL:function(){return p},zk:function(){return n}});var l=t(2884);const u=e=>{const a={page_num:1,page_size:1};return a.page_num=e.page_num,a.page_size=e.page_size,l.Z.get(`/poc/${a.page_num}/${a.page_size}`)},n=()=>l.Z.get("/poc/sync"),p=e=>{const a={query:""};return""==e.query?a.query="null":a.query=e.query,l.Z.get(`/poc/treepoc/${a.query}`)}},2011:function(e,a,t){t.r(a),t.d(a,{default:function(){return g}});var l=t(3396),u=t(4870);const n=[{prop:"id",label:"序号",width:75},{prop:"parent",label:"应用",width:250},{prop:"name",label:"漏洞名称",width:200},{prop:"type",label:"漏洞类别",width:100},{prop:"number",label:"漏洞编号",width:200},{prop:"info",label:"漏洞信息",width:200}];var p=t(7237),r=t(7178);const s={class:"demo-pagination-block pagination-right"};var o=(0,l.aZ)({__name:"PocManage",setup(e){const a=(0,u.iH)(!1),t=(0,u.iH)(!1),o=(0,u.iH)(!1),i=(0,u.iH)([]),c=(0,u.iH)(),g=(0,u.iH)({page_size:50,page_num:1}),d=async()=>{await(0,p.zk)().then((()=>{(0,r.z8)({message:"同步POC成功",type:"success"})}),(e=>{(0,r.z8)({message:"同步POC失败",type:"error"})})),_()},_=async()=>{const e=await(0,p.A7)(g.value);i.value=e.data.pocs,c.value=e.data.total};_();const m=e=>{g.value.page_num=1,g.value.page_size=e,_()},v=e=>{g.value.page_num=e,_()};return(e,p)=>{const r=(0,l.up)("el-button"),_=(0,l.up)("el-col"),w=(0,l.up)("el-row"),b=(0,l.up)("el-table-column"),z=(0,l.up)("el-table"),h=(0,l.up)("el-pagination"),y=(0,l.up)("el-card");return(0,l.wg)(),(0,l.j4)(y,{class:"card"},{default:(0,l.w5)((()=>[(0,l.Wm)(w,{class:"row"},{default:(0,l.w5)((()=>[(0,l.Wm)(_,{span:3},{default:(0,l.w5)((()=>[(0,l.Wm)(r,{type:"primary",size:"small",onClick:d},{default:(0,l.w5)((()=>[(0,l.Uk)("同步POC")])),_:1})])),_:1})])),_:1}),(0,l.Wm)(z,{data:i.value,style:{width:"100%"},size:"small"},{default:(0,l.w5)((()=>[((0,l.wg)(!0),(0,l.iD)(l.HY,null,(0,l.Ko)((0,u.SU)(n),((e,a)=>((0,l.wg)(),(0,l.j4)(b,{prop:e.prop,label:e.label,width:e.width,key:a},null,8,["prop","label","width"])))),128))])),_:1},8,["data"]),(0,l._)("div",s,[(0,l.Wm)(h,{"current-page":g.value.page_num,"onUpdate:current-page":p[0]||(p[0]=e=>g.value.page_num=e),"page-size":g.value.page_size,"onUpdate:page-size":p[1]||(p[1]=e=>g.value.page_size=e),"page-sizes":[50,100,150],small:a.value,disabled:o.value,background:t.value,total:c.value,layout:"total, sizes, prev, pager, next, jumper",onSizeChange:m,onCurrentChange:v,class:"navbar-right"},null,8,["current-page","page-size","small","disabled","background","total"])])])),_:1})}}}),i=t(89);const c=(0,i.Z)(o,[["__scopeId","data-v-031560c4"]]);var g=c}}]);
//# sourceMappingURL=11.8097a021.js.map