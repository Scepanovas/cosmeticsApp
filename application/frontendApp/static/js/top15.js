mainApp.controller('Top15Ctrl', function($scope, $http)
{
  $scope.init = function()
  {
    $scope.loadTop15('/api/topproducts/', 'P');
    $scope.loadTop15('/api/topbrands/',   'B');
    $scope.loadTop15('/api/topusers/',    'U');
  };
  $scope.loadTop15 = function(url, type)
  {
    $http.get(url).then(function(response){
       var resultsData = {};
       resultsData = response.data;
       switch(type){
         case 'P':
           $scope.products = resultsData;
           if (resultsData.length > 0){
             $scope.productsExist = true;
           } else {
             $scope.productsExist = false;
           }
           break;
         case 'B':
           $scope.brands = resultsData;
           if (resultsData.length > 0){
             $scope.brandsExist = true;
           } else {
             $scope.brandsExist = false;
           }
           break;
         case 'U':
           $scope.users = resultsData;
           if (resultsData.length > 0){
             $scope.usersExist = true;
           } else {
             $scope.usersExist = false;
           }
           break;
       };
    });
  };
});
