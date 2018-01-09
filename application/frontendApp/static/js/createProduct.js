mainApp.controller('CreateProductCtrl', function($scope, $http, toaster,
                                                 createProductFactor, patchProductFactor)
{
  $scope.init = function(url, action, productSearchUrl)
  {
    $scope.url                     = url;
    $scope.action                  = action;
    $scope.productSearchUrl        = productSearchUrl;
    $scope.searchResults           = {};
    $scope.searchResults.count     = 0;
    $scope.searchResults.results   = []
    $scope.value                   = '';
    $scope.pageNo                  = 0;
    $scope.lastPage                = 0;
    $scope.search($scope.value);
    $scope.recordsExist            = false;
    $scope.attachedIngredients     = [];
    $scope.newProductModel         = {};
    $scope.newProductModel.tagLine = "";

  };
  $scope.safeApply = function(fn) {
    var phase = this.$root.$$phase;
    if(phase == '$apply' || phase == '$digest') {
      if(fn && (typeof(fn) === 'function')) {
        fn();
      }
    } else {
      this.$apply(fn);
    }
  };
  $scope.postProduct = function(form)
  {
      createProductFactor.create(form).$promise.then(
          function(response) {
              toaster.pop('success', "Produktas sukurtas sėkmingai!");
              $scope.patchProductDetails.pk = response.pk;
              $scope.patchRecord($scope.patchProductDetails);
              $scope.newProductModel = {};
              $scope.attachedIngredients = [];
              var image = document.getElementById('imagePreview');
              image.parentNode.removeChild(image);
              document.getElementById("files").value = "";
              $scope.newProductModel.tagLine = "";
          },
          function(rejection) {
              toaster.pop('error', "Produkto sukurti nepavyko");
              console.log(rejection);
          }
      );
  };
  $scope.patchRecord = function(patchObject)
  {
      patchProductFactor.put(patchObject).$promise.then(
          function(response) {
          },
          function(rejection) {
              toaster.pop('error', "Nepavyko pridėti ingredientų");
              console.log(rejection);
          }
      );
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
    if (page+1 < $scope.lastPage){
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
  $scope.alreadyAdded = function (array, key, value) {
    for (var i = 0; i < array.length; i++) {
        if (array[i][key] === value) {
            return true;
        }
    };
    return false;
  };
  $scope.alreadyExist = async function(url, value)
  {
    const result = await $http.get(url + value);
    return (result.data.length > 0);
  };
  $scope.addIngredient = function(pk, name)
  {
    if ($scope.alreadyAdded($scope.attachedIngredients, 'pk', pk))
    {
      toaster.pop('error', "Ingredientas jau yra pridėtas");
    } else {
      $scope.attachedIngredients.push({pk, name});
    };
  };
  $scope.remIngredient = function(pk)
  {
    var index;
    $scope.attachedIngredients.some(function(entry, i) {
    if (entry.pk == pk) {
        index = i;
        return true;
      }
    });
    $scope.attachedIngredients.splice(index, 1);
  };
  $scope.createProduct = async function(brandPk)
  {
    $scope.errors = {};
    $scope.productDetails = {};
    $scope.patchProductDetails = {};
    $scope.noErrorsFound = true;
    ingredientsList = [];
    ingredientsList = $scope.attachedIngredients.map(function(a) {return a.pk;});
    /*arr str to arr int
    ingredientsList = ingredientsList.map(Number);*/

    if (typeof $scope.myFile !== 'undefined') {
      if ($scope.myFile.type.substring(0,5) == "image")
      {
        $scope.productDetails.image = $scope.myFile;
      } else {
        $scope.errors.image = 'Netinkamas paveikslėlio tipas';
        $scope.noErrorsFound   = false;
      }
    }
    else
    {
      $scope.errors.image = 'Pridėkite paveikslėlį';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.newProductModel.tagLine === 'undefined') {
      $scope.errors.tagLine = 'Kuriant produktą privaloma įvesti aprašymą';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.newProductModel.name === 'undefined') {
      $scope.errors.name = 'Kuriant produktą privaloma įvesti pavadinimą';
      $scope.noErrorsFound   = false;
    } else {
      if ($scope.newProductModel.name.length > 4)
      {
        if (await $scope.alreadyExist($scope.productSearchUrl, $scope.newProductModel.name))
        {
          $scope.errors.name = 'Produktas su tokiu pavadinimu jau egzistuoja';
          $scope.noErrorsFound   = false;
        } else {
          $scope.productDetails.name = $scope.newProductModel.name;
        };
      } else {
        $scope.errors.name = 'Produkto pavadinimą turi sudaryti bent 5 ženklai';
        $scope.noErrorsFound   = false;
      };
    };
    if (ingredientsList.length == 0)
    {
      $scope.errors.ingredients = 'Nepasirinkote ingredientų';
      $scope.noErrorsFound   = false;
    } else {
      $scope.patchProductDetails.ingredients = ingredientsList;
      $scope.productDetails.ingredients = [763];
    };
    $scope.productDetails.tagLine = $scope.newProductModel.tagLine;
    $scope.productDetails.brand   = brandPk;
    $scope.safeApply($scope);
    if ($scope.noErrorsFound)
    {
      $scope.postProduct($scope.productDetails);
    } else {
      toaster.pop('error', "Produkto kūrimo formoje yra klaidų");
    };
  };
});
