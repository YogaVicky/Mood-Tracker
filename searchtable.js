function searchTable() {
	  var input, filter, table, tr, td, i,txtValue,td2,txtValue2,td3,txtValue3;
	  input = document.getElementById("search");
	  filter = input.value.toUpperCase();
	  table = document.getElementById("main");
	  tr = table.getElementsByTagName("tr");
	  console.log(input); 
	    for (i = 0; i < tr.length; i++) {

	    td = tr[i].getElementsByTagName("td")[0];
	    if (td) {
	      txtValue = td.textContent || td.innerText;
	      if (txtValue.toUpperCase().indexOf(filter) > -1) {
	        tr[i].style.display = "";
	      } else {
	        tr[i].style.display = "none";
	      }
	    }
	  }
	}
