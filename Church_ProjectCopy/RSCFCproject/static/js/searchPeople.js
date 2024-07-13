let present = [];

document.getElementById("switchCount").innerHTML = `
${present.length}
  `;

var switchs = document.querySelectorAll(".switch");

switchs.forEach((item) => {
  item.addEventListener("click", (event) => {
    const value = event.target.id;
    if (event.target.checked) {
      present.push(event.target.id);
      document.getElementById("switchCount").innerHTML = `

   ${present.length}
  `;
  document.getElementById('id_extra_field').value = present;
      console.log(present);
    } else {
      let updated = present.filter((item) => {
        return item !== value;
      });
      present = updated;
      document.getElementById("switchCount").innerHTML = `

   ${present.length}
  `;
  document.getElementById('extra_field').value = present;
      console.log(present);
    }
  });
});


const searchField = document.querySelector("#searchField");

const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
tableOutput.style.display = "none";
const noResults = document.querySelector(".no-results");
noResults.style.display = "none";
const tbody = document.querySelector('.table-body')

searchField.addEventListener("keyup", (e) => {
		const searchValue = e.target.value;

		if (searchValue.length > 0) {
			tbody.innerHTML = "";
			

		fetch("search-group", {
			body: JSON.stringify({ searchText: searchValue }),
			method: "POST",
		})
			.then((res) => res.json())
			.then((data) => {
				appTable.style.display = "none";
				tableOutput.style.display = "block";

			if (data.length===0) {
				noResults.style.display = 'block';
				tableOutput.style.display = 'none';
			} else {
				noResults.style.display = 'none'
					data.forEach((item) => {
						tbody.innerHTML += `
						<tr>

							<td><a href="person/${item.id}"> ${item.Name} ${item.Surname}</a></td>
							<td>${item.Gender}</td>
							<td><a class="form-check form-switch">
							<input class="form-check-input switch" type="checkbox" name="" id="${item.id}">
							<label class="form-check-label" for="flexSwitchCheckDefault">Absent/Present</label></td>



						</tr>`;


						
					})
				}
			});

			console.log(switchs);
			updateEventListner();	
		} else {
			tableOutput.style.display = "none";
			appTable.style.display = "block";
			
			
		}
			
}


);

function updateEventListner() {


	console.log("Updated Events");
  
	  switchs.forEach((item) => {
		item.addEventListener("click", (event) => {
		  const value = event.target.id;
	  console.log("Button Press");
		  if (event.target.checked) {
			present.push(event.target.id);
			document.getElementById("switchCount").innerHTML = `
	  
		Attendance ${present.length}
		`;
			console.log(present);
		  } else {
			let updated = present.filter((item) => {
			  return item !== value;
			});
			present = updated;
			document.getElementById("switchCount").innerHTML = `
	  
		Attendance ${present.length}
		`;
			console.log(present);
		  }
		});
	  });}