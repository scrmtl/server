import jsPDF from "jspdf";
import "jspdf-autotable";
import { mapGetters } from "vuex";
export default {
  computed: {
    ...mapGetters("task", {
      taskByIdArray: "byIdArray",
    }),

    ...mapGetters("sprintStatistics", {
      sprintStatistic: "bySprintId",
    }),
  },

  methods: {
    createReport(sprint, img) {
      console.log(img);
      let pdfName = "ReportSprint" + sprint.number;
      var doc = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "a4"
      });
      // text is placed using x, y coordinates
      doc.setFontSize(16).text("Report Sprint " + sprint.number, 10, 20);
      //Generate todays date
      var today = new Date();
      var dd = String(today.getDate()).padStart(2, '0');
      var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
      var yyyy = today.getFullYear();
      today = mm + '/' + dd + '/' + yyyy;
      doc.setFontSize(7).text("Created on " + today, 175, 23);
      // create a line under heading 
      doc.setLineWidth(0.01).line(10, 25, 200, 25);
      // Table with Infos of Sprint (https://github.com/simonbengtsson/jsPDF-AutoTable/blob/master/examples/examples.js)
      var finalY = doc.lastAutoTable.finalY || 40;
      doc.autoTable({
        startY: finalY,
        head: [['Information', ' ']],
        body: this.GetInformation(sprint),
        headStyles: { fillColor: "#6441A4" },
      })

      //Summary als Tabelle
      doc.autoTable({
        startY: doc.lastAutoTable.finalY + 20,
        head: [['Summary', ' ']],
        body: this.GetSummary(sprint),
        headStyles: { fillColor: "#6441A4" },
      })
      
      //zweite Seite Hinzufügen
      doc.addPage();

      //nochmal den Header
      doc.setFontSize(16).text("Report Sprint " + sprint.number, 10, 20);
      doc.setFontSize(7).text("Created on " + today, 175, 23);
      // create a line under heading 
      doc.setLineWidth(0.01).line(10, 25, 200, 25);


      //Sprint Details als Tabelle
      doc.setFontSize(12).text("Sprint Details", 10, finalY = 40);
      doc.autoTable({
        startY: finalY + 2,
        head: [["ID", "Task Name", "Description", "SP", "Status"]],
        body: this.GetDetails(sprint),
        headStyles: { fillColor: "#6441A4" },
      })

      doc.save(`${pdfName}.pdf`);


    },

    GetInformation(sprint) {
      var informationArray = [];
      var currentDate = new Date();
      var generatedDate = currentDate.toLocaleDateString() + " - " + currentDate.toTimeString();
      informationArray.push(["Sprint No.", sprint.number]);
      informationArray.push(["Status", this.GetNamedStatus(sprint.status)]);
      informationArray.push(["Start", sprint.start]);
      informationArray.push(["End", sprint.end]);
      informationArray.push(["Total Duration", sprint.total_duration]);
      if (sprint.status !== "DO" || sprint.status !== "AC") {
        informationArray.push(["Remaining Duration", sprint.remaining_duration]);
      }
      informationArray.push(["Product Version", sprint.version]);
      informationArray.push(["Story", sprint.story]);
      informationArray.push(["Report Generated", generatedDate]);
      return informationArray;
    },

    GetSummary(sprint) {
      var summaryArray = [];
      var statistic = this.sprintStatistic(sprint.id);
      // storpoints
      summaryArray.push(["Planned Storypoints", statistic.sum_of_sp + " SP"]);
      if (sprint.status === "DO" || sprint.status === "AC") {
        summaryArray.push(["Accepted Storypoints", statistic.sum_of_accepted_sp + " SP"]);
      }
      else {
        summaryArray.push(["Done Storypoints", statistic.sum_of_done_sp + " SP"]);
        summaryArray.push(["Not Done Storypoints", (statistic.sum_of_sp - statistic.sum_of_done_sp) + " SP"]);
      }
      // Tasks
      summaryArray.push(["Planned Tasks", statistic.sum_of_tasks]);
      if (sprint.status === "DO" || sprint.status === "AC") {
        summaryArray.push(["Accepted Tasks", statistic.sum_of_accepted_tasks]);
      }
      else {
        summaryArray.push(["Done Tasks", statistic.sum_of_done_tasks]);
        summaryArray.push(["Not Done Tasks", (statistic.sum_of_tasks - statistic.sum_of_done_tasks)]);
      }
      return summaryArray;
    },

    GetDetails(sprint) {
      var detailArray = [];
      var tasks = this.taskByIdArray(sprint.task_cards);
      tasks.forEach(task => {
        detailArray.push([task.id, task.name, task.description, task.storypoints, this.GetNamedStatus(task.status)])
      });

      return detailArray;
    },

    GetNamedStatus(status) {
      var namedStatus = "in Planning";
      // all available Status of task and Sprint!!!
      switch (status) {
        case "IL":
          namedStatus = "In Planning";
          break;
        case "PL":
          namedStatus = "Planned";
          break;
        case "IR":
          namedStatus = "In Progress";
          break;
        case "DO":
          namedStatus = "Done";
          break;
        case "AC":
          namedStatus = "Accepted";
          break;
        case "NW":
          namedStatus = "New";
          break;
        case "NS":
          namedStatus = "Not Started";
          break;
        case "IP":
          namedStatus = "In Progress";
          break;
        case "DE":
          // If the task declined from PO, is a workflow nessesary
          namedStatus = "Declined";
          break;

      }
      return namedStatus;
    },
  }
}