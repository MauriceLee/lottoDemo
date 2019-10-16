<template>
  <div id="home">
    <b-container>
      <b-table
        striped
        :items="lottoData"
      ></b-table>
      <div
        class="d-flex"
        style="margin-top: 30px;"
      >
        <b-table
          v-for="(item, index) in winNumProb"
          :key="index"
          :items="item"
        ></b-table>
      </div>
    </b-container>
  </div>
</template>

<script>
  export default {
    data: () => ({
      lottoData: [],
      winNumProb: []
    }),
    mounted() {
      this.axios.get("data_Info_Dict.json").then(res => {
        Object.keys(res.data).forEach(item => {
          this.lottoData.push(res.data[item]);
        });
        let winNums = [].concat(
          ...this.lottoData.map(item => item.winning_numbers)
        );
        let winNumCount = {};
        winNums.forEach(item => {
          winNumCount[item] = (winNumCount[item] || 0) + 1;
        });
        let tempWinNumProb = [];
        for (let i = 0; i < 49; i++) {
          tempWinNumProb.push({ 號碼: `${i + 1}`, 機率: "0" });
        }
        Object.keys(winNumCount).forEach(item => {
          tempWinNumProb[item - 1].機率 = (
            (winNumCount[item] / 70) *
            100
          ).toFixed(2);
        });
        tempWinNumProb = tempWinNumProb.sort((a, b) =>
          a.機率 > b.機率 ? -1 : 1
        );
        for (let i = 0; i < 7; i++) {
          this.winNumProb.push(tempWinNumProb.slice(i * 7, (i + 1) * 7));
        }
      });
    }
  };
</script>

<style>
  .table th,
  .table td {
    padding: 0.6rem;
    border: 1px solid #dee2e6;
  }
</style>