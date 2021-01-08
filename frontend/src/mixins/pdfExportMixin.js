import jsPDF from "jspdf";
import { mapGetters } from "vuex";
export default {
  computed:{
    ...mapGetters("sprint", {
      listSprints: "list",
    }),

    ...mapGetters("sprintStatistics", {
      sprintStatistic: "bySprintId",
    }),
  },

  methods:{
    createReport(sprint){
      let pdfName = "ReportSprint" +sprint.number;
      var doc = new jsPDF ( {
        orientation: "portrait",
        unit: "mm",
        format: "a4"
      });
      // text is placed using x, y coordinates
      doc.setFontSize(16).text("Report Sprint " +sprint.number, 10, 20);
      // create a line under heading 
      doc.setLineWidth(0.01).line(10, 25, 200, 25);
      doc.save(`${pdfName}.pdf`);


    }
  }
}