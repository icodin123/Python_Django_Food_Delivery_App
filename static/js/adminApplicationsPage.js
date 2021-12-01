// API for managing UI for admin portal applications page

function SchoolApplication(name, address, date){
  this.name = name;
  this.address = address;
  this.date = date;
}

function RestaurantApplication(name, address, date){
  this.name = name;
  this.address = address;
  this.date = date;
}

let mockSchoolApplications = [new SchoolApplication('St. John School',
'101, Chinatown', '2019/09/01'), new SchoolApplication('St. George School',
'102, Chinatown', '2019/09/02'), new SchoolApplication('St. Mike School',
'103, Chinatown', '2019/09/03')];

let mockRestaurantApplications = [
  new RestaurantApplication('Red Dragon 1', '101 College Street', '2019/11/01'),
  new RestaurantApplication('Red Dragon 2', '102 College Street', '2019/11/02'),
  new RestaurantApplication('Red Dragon 3', '103 College Street', '2019/11/03')
];

function ApplicationPageManager(schoolApps, restaurantApps){

  this.loadApplications = function(schoolApplications, restaurantApplications){

    for(let i = 0; i < schoolApplications.length; i++){
      this.loadSchoolApplication(schoolApplications[i]);
    }

    for(let j = 0; j < restaurantApplications.length; j++){
      this.loadRestaurantApplication(restaurantApplications[j]);
    }

  }

  this.loadSchoolApplication = function(givenSchool){

    let schoolTable = document.querySelector('#schoolTable');

    let newTr = document.createElement('tr');

    let newTd1 = document.createElement('td');
    newTd1.textContent = givenSchool.name;

    let newTd2 = document.createElement('td');
    newTd2.textContent = givenSchool.address;

    let newTd3 = document.createElement('td');
    newTd3.textContent = givenSchool.date;

    let newTd4 = document.createElement('td');

    let reviewButton = document.createElement('button');
    reviewButton.className = 'reviewButton';
    reviewButton.textContent = 'View profile';

    newTd4.appendChild(reviewButton);

    newTr.appendChild(newTd1);
    newTr.appendChild(newTd2);
    newTr.appendChild(newTd3);
    newTr.appendChild(newTd4);

    schoolTable.appendChild(newTr);

  }

  this.loadRestaurantApplication = function(givenRestaurant){

    let restaurantTable = document.querySelector('#restaurantTable');

    let newTr = document.createElement('tr');

    let newTd1 = document.createElement('td');
    newTd1.textContent = givenRestaurant.name;

    let newTd2 = document.createElement('td');
    newTd2.textContent = givenRestaurant.address;

    let newTd3 = document.createElement('td');
    newTd3.textContent = givenRestaurant.date;

    let newTd4 = document.createElement('td');

    let reviewButton = document.createElement('button');
    reviewButton.className = 'reviewButton';
    reviewButton.textContent = 'View profile';

    newTd4.appendChild(reviewButton);

    newTr.appendChild(newTd1);
    newTr.appendChild(newTd2);
    newTr.appendChild(newTd3);
    newTr.appendChild(newTd4);

    restaurantTable.appendChild(newTr);

  }

}


let applicationsPageManager = new ApplicationPageManager();
window.onload = function () {
  applicationsPageManager.loadApplications(mockSchoolApplications,
    mockRestaurantApplications);
};
