mainApp.controller('SearchCtrl', function($scope, $http)
{
  $scope.init = function(url, action)
  {
    $scope.url                    = url;
    $scope.action                 = action;
    $scope.searchResults          = {};
    $scope.searchResults.count    = 0;
    $scope.searchResults.results  = []
    $scope.value                  = '';
    $scope.pageNo                 = 0;
    $scope.lastPage               = 0;
    $scope.search($scope.value);
    $scope.recordsExist           = false;
  };
  $scope.changeSign = function(showDetails, index)
  {
    var id = "sign" + index;
    if (showDetails)
    {
      document.getElementById(id).innerHTML = "-";
    } else {
      document.getElementById(id).innerHTML = "+";
    };
  };
  $scope.getSearchResults = function(url, action, value, page, viaSearch) {
     $http.get(url + action + value).then(function(response){
        $scope.searchResults = response.data;
        $scope.lastPage = $scope.searchResults.count/10 >> 0;
        if (($scope.searchResults.count % 10) > 0){
          $scope.lastPage += 1;
        };
        if (viaSearch){
          $scope.setPage(page, viaSearch);
          if ($scope.searchResults.count > 0){
            $scope.recordsExist = false;
          } else {
            $scope.recordsExist = true;
          };
        };
    });
  };
  $scope.setPage = function(page, viaSearch){
    var tempPageList = [];
    if (typeof page !== 'number'){
      page = page.replace(/[^\d]/g, '');
    };
    if (page == '' || page > $scope.lastPage ||
       ($scope.pageNo == page & !viaSearch)) {
      return false;
    };
    $scope.pageNo   = page;
    tempPageList = ["<<" + page + ">>"];
    for (i = 1; i < 3; i++){
      if (page-i > 0){
        tempPageList.unshift(page-i);
      };
    };
    for (i = 1; i < 3; i++){
      if (page+i <= $scope.lastPage){
      tempPageList.push(page+i)
      };
    };
    if (page-3 > 0){
      tempPageList.unshift(" .. ");
      for (i = 3; i > 0; i--){
        if (page-2 > i){
          tempPageList.unshift(i);
        };
      };
    };
    if (page+2 < $scope.lastPage){
      tempPageList.push(" .. ");
      for (i = $scope.lastPage - 1; i <= $scope.lastPage; i++){
        if (i > page+1){
          tempPageList.push(i);
        };
      };
    };
    $scope.pageList = tempPageList;
    return true;
  };
  $scope.search = function(value){
     if (value !== undefined){
       $scope.value = value;
     };
     $scope.getSearchResults($scope.url, $scope.action, $scope.value, 1, true);
  };
  $scope.anotherPage = function(page){
     if ($scope.setPage(page, false)){
       var action = "?page=" + page +"&search=";
       $scope.getSearchResults($scope.url, action, $scope.value, NaN, false);
     };
  };
});
