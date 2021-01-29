<template>
  <div ref="container" class="vue-plotly" v-resize:debounce.100="onResize" />
</template>

<script>
import Plotly from "plotly.js/lib/core";
import PlotlyScatter from "plotly.js/lib/scatter";
import PlotlyHistogram from "plotly.js/lib/histogram";
import PlotlySurface from "plotly.js/lib/surface";
import PlotlyTreemap from "plotly.js/lib/treemap";
import PlotlyBar from "plotly.js/lib/bar";

Plotly.register([
  PlotlyScatter,
  PlotlyHistogram,
  PlotlySurface,
  PlotlyTreemap,
  PlotlyBar,
]);

import resize from "vue-resize-directive";

import ExcelJS from "exceljs";

const events = [
  "click",
  "hover",
  "unhover",
  "selecting",
  "selected",
  "restyle",
  "relayout",
  "autosize",
  "deselect",
  "doubleclick",
  "redraw",
  "animated",
  "afterplot",
  "treemapclick",
];

const functions = [
  "restyle",
  "relayout",
  "update",
  "addTraces",
  "deleteTraces",
  "moveTraces",
  "extendTraces",
  "prependTraces",
  "purge",
];

const methods = functions.reduce((all, funcName) => {
  all[funcName] = function (...args) {
    return Plotly[funcName].apply(Plotly, [this.$refs.container].concat(args));
  };
  return all;
}, {});

export default {
  directives: {
    resize,
  },

  props: {
    autoResize: Boolean,
    options: Object,
    data: Array,
    layout: Object,
    limitAxis: Boolean,
    download: Boolean,
  },

  data() {
    return {
      internalLayout: {
        ...this.layout,
        datarevision: 1,
      },
    };
  },

  mounted() {
    this.newPlot();
    this.initEvents();
  },

  watch: {
    data: {
      handler() {
        this.internalLayout.datarevision++;
        this.react().then(() => {});
      },
      deep: true,
    },
    options: {
      handler() {
        this.react();
      },
      deep: true,
    },
    layout: {
      handler() {
        this.internalLayout = Object.assign(this.internalLayout, this.layout);
        this.react();
      },
      deep: true,
    },
  },

  beforeDestroy() {
    this.__generalListeners.forEach((obj) =>
      this.$refs.container.removeAllListeners(obj.fullName)
    );
    Plotly.purge(this.$refs.container);
  },

  methods: {
    initEvents() {
      this.__generalListeners = events.map((eventName) => {
        return {
          fullName: "plotly_" + eventName,
          handler: (...args) => this.$emit.apply(this, [eventName, ...args]),
        };
      });
      this.__generalListeners.forEach((obj) => {
        this.$refs.container.on(obj.fullName, obj.handler);
      });

      this.$refs.container.on("plotly_relayout", this.limitAxisHandler);
    },

    onResize() {
      if (this.autoResize && this.$refs.container) {
        this.internalLayout.datarevision++;
        Plotly.Plots.resize(this.$refs.container);
      }
    },

    ...methods,

    plot() {
      return Plotly.plot(
        this.$refs.container,
        this.data,
        this.internalLayout,
        this.getOptions()
      );
    },

    getOptions() {
      let el = this.$refs.container;
      let opts = this.options;
      // if width/height is not specified for toImageButton, default to el.clientWidth/clientHeight
      if (!opts) opts = {};
      if (!opts.toImageButtonOptions) opts.toImageButtonOptions = {};
      if (!opts.toImageButtonOptions.width)
        opts.toImageButtonOptions.width = el.clientWidth;
      if (!opts.toImageButtonOptions.height)
        opts.toImageButtonOptions.height = el.clientHeight;

      if (this.download) {
        if (!opts.modeBarButtons) opts.modeBarButtons = [[]];

        opts.modeBarButtons[0].push({
          name: "download",
          title: "Download",
          click: this.saveXlsx,
          icon: {
            width: 857.1,
            height: 1000,
            path:
              "m214-7h429v214h-429v-214z m500 0h72v500q0 8-6 21t-11 20l-157 156q-5 6-19 12t-22 5v-232q0-22-15-38t-38-16h-322q-22 0-37 16t-16 38v232h-72v-714h72v232q0 22 16 38t37 16h465q22 0 38-16t15-38v-232z m-214 518v178q0 8-5 13t-13 5h-107q-7 0-13-5t-5-13v-178q0-8 5-13t13-5h107q7 0 13 5t5 13z m357-18v-518q0-22-15-38t-38-16h-750q-23 0-38 16t-16 38v750q0 22 16 38t38 16h517q23 0 50-12t42-26l156-157q16-15 27-42t11-49z",
            transform: "matrix(1 0 0 -1 0 850)",
          },
        });
      }

      opts.responsive = false;

      return opts;
    },

    newPlot() {
      return Plotly.newPlot(
        this.$refs.container,
        this.data,
        this.internalLayout,
        this.getOptions()
      );
    },

    react() {
      return Plotly.react(
        this.$refs.container,
        this.data,
        this.internalLayout,
        this.getOptions()
      );
    },

    fxHover(evt, subplot) {
      return Plotly.Fx.hover(this.$refs.container, evt, subplot);
    },

    limitAxisHandler(evt) {
      if (this.limitAxis) {
        let updObj = {};

        let idx = 1;
        let name = "xaxis";
        let nameShort = "x";

        while (this.internalLayout[name]) {
          if (evt[name + ".range[0]"] && evt[name + ".range[1]"]) {
            let actMin = evt[name + ".range[0]"];
            let actMax = evt[name + ".range[1]"];

            if (
              this.internalLayout[name].type &&
              this.internalLayout[name].type == "date"
            ) {
              actMin = new Date(actMin).getTime();
              actMax = new Date(actMax).getTime();
            }

            let min = Number.MAX_VALUE;
            let max = -Number.MAX_VALUE;

            this.data.forEach((trace) => {
              if (
                (trace.xaxis && trace.xaxis == nameShort) ||
                (idx == 1 && !trace.xaxis)
              ) {
                min = Math.min(min, ...trace.x);
                max = Math.max(max, ...trace.x);
              }
            });

            let newMin = actMin;
            let newMax = actMax;

            if (actMin < min) {
              newMin = min;
            }

            if (actMax > max) {
              newMax = max;
            }

            if (newMax - newMin != actMax - actMin) {
              newMax = newMin + actMax - actMin;

              if (newMax > max) {
                newMin -= newMax - max;
              }
            }

            if (newMin < min) {
              newMin = min;
            }

            if (newMax > max) {
              newMax = max;
            }

            if (newMin != actMin) {
              updObj[name + ".range[0]"] = newMin;
            }

            if (newMax != actMax) {
              updObj[name + ".range[1]"] = newMax;
            }
          }

          idx++;
          name = "xaxis" + idx.toString();
          nameShort = "x" + idx.toString();
        }

        if (Object.keys(updObj).length > 0) {
          this.relayout(updObj);
        }
      }
    },

    async saveXlsx() {
      let data = {};

      this.data.forEach((pd) => {
        if (pd.exportName) {
          pd.x.forEach((x, idx) => {
            if (!data[x]) data[x] = {};

            data[x][pd.exportName] =
              pd.y[idx] instanceof Date ? pd.y[idx].getTime() : pd.y[idx];
          });
        }
      });

      let cols = [];

      let dataArray = Object.keys(data)
        .map((key) => {
          Object.keys(data[key]).forEach((k) => {
            if (!cols.includes(k)) cols.push(k);
          });

          let time = new Date();
          time.setTime(key);

          return {
            time,
            ...data[key],
          };
        })
        .sort((a, b) => a.time.getTime() - b.time.getTime());

      let lastVals = {};

      dataArray.forEach((d) => {
        cols.forEach((c) => {
          if (lastVals[c] == undefined && d[c] != undefined && d[c] != null) {
            lastVals[c] = d[c];
          }
        });
      });

      dataArray.forEach((d) => {
        cols.forEach((c) => {
          if (d[c] == undefined || d[c] == null) {
            d[c] = lastVals[c];
          } else {
            lastVals[c] = d[c];
          }
        });
      });

      cols.unshift("time");

      let wb = new ExcelJS.Workbook();
      let sheet = wb.addWorksheet("export", {
        views: [{ state: "frozen", ySplit: 1 }],
      });

      cols.forEach((c, idx) => {
        let cell = sheet.getCell(1, idx + 1);
        cell.value = c;
        cell.font = { bold: true };

        dataArray.forEach((d, dIdx) => {
          cell = sheet.getCell(dIdx + 2, idx + 1);

          if (d[c] instanceof Date) {
            cell.value = d[c].toLocaleString();
          } else {
            cell.value = d[c];
          }
        });
      });

      let buf = await wb.xlsx.writeBuffer();

      this.saveFile(buf, "export.xlsx");
    },
  },
};
</script>