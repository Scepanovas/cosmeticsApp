mainApp.controller('ViewProductCtrl', function($scope, $http, toaster,
                                               patchProductFactor, postComment,
                                               $sce, patchRatingFactor,
                                               postRatingFactor)
{
  $scope.getId = function(url)
  {
    var urlLength = url.length;
    var urlLast   = url.lastIndexOf('/')+1;
    if (urlLength == urlLast){ url = url.substring(0,urlLength-1); };
    urlLast = url.lastIndexOf('/')+1;
    var id = url.substring(urlLast);
    if (isNaN(id)){ id = 0; }
    return id;
  };
  $scope.patchRecord = function(patchObject)
  {
      patchProductFactor.put(patchObject).$promise.then(
          function(response) {
            toaster.pop('success', "Informacija atnaujinta!");
            if ($scope.productDetails.tagLine != response.tagLine)
            {
              $scope.productDetails.tagLine = response.tagLine;
            };
          },
          function(rejection) {
            toaster.pop('error', "Nepavyko atnaujinti informacijos");
            console.log(rejection);
          }
      );
  };
  $scope.init = function(customerId, url)
  {
    $scope.productDetails = {};
    $scope.ingredientsEditMode = false;
    $scope.tagLineEditMode = false;
    $scope.customerId = customerId;
    if ($scope.customerId != undefined) {
      $scope.getUserDetails($scope.customerId);
    };
    $scope.url = url;
    $scope.currentUrl = window.location.href;
    $scope.Id = $scope.getId($scope.currentUrl);
    $scope.productExist = true;
    $scope.ingredientsChagned = false;
    $scope.functionsList = [];
    $scope.warningsList = [];
    $scope.suggestedList = [];
    $scope.notSuggestedList = [];
    $scope.suggestedListEmpty = true;
    $scope.notSuggestedListEmpty = true;
    $scope.comment = {};
    $scope.searchComments('?search=', $scope.Id);
    $scope.setPage(1, true, true);
    $scope.alreadyRatedBool = false;
    $scope.currentAvgRating = 0;
    $scope.currentAvgRating = $scope.currentAvgRating.toFixed(1);

    if ($scope.Id == 0){
      $scope.productExist = false;
    } else {
      $scope.alreadyRated($scope.Id, $scope.customerId);
      $scope.getCurrentAvgRating($scope.Id);
      $http.get($scope.url + $scope.Id).then(
        function(response){
          $scope.productDetails = response.data;
          if ($scope.productDetails.brand.pk == customerId){
            $scope.editable = true;
          };
          if ($scope.productDetails.brand.webPage.substring(0, 6) == 'http://'){
            $scope.officialUrl = $scope.productDetails.brand.webPage;
          } else {
            $scope.officialUrl = 'http://' + $scope.productDetails.brand.webPage;
          };
          $scope.generateFunctionsList ($scope.productDetails.ingredients);
          $scope.generateWarningsList  ($scope.productDetails.ingredients);
          if ($scope.userDetails != undefined){
            if ($scope.userDetails.skinType != null &&
                $scope.userDetails.skinType != 0)
            {
              $scope.generateSuggestionList($scope.userDetails.skinType, $scope.functionsList);
            };
          };
        },
        function(data) {
          $scope.productExist = false;
        });
    };
  };
  $scope.generateSuggestionList = function(userData, productData) {
    console.log(userData);
    console.log(productData);
    for (var i = 0; i < userData.suggested.length; i++){
      for (var j = 0; j < productData.length; j++){
        if (userData.suggested[i].function == productData[j].pk)
        {
          $scope.suggestedList.push(userData.suggested[i]);
          $scope.suggestedListEmpty = false;
        };
      };
    };
    for (var i = 0; i < userData.notSuggested.length; i++){
      for (var j = 0; j < productData.length; j++){
        if (userData.notSuggested[i].function == productData[j].pk)
        {
          $scope.notSuggestedList.push(userData.notSuggested[i]);
          $scope.notSuggestedListEmpty = false;
        };
      };
    };
  };
  $scope.getUserDetails = function(id){
    $http.get('/api/brandDetails/' + id).then(function(response){
      $scope.userDetails = response.data;
    });
  };
  $scope.rate = function(ratingIn, brand){
    var patchObject = {};
    if ($scope.alreadyRatedBool){
      patchObject.pk           = $scope.alreadyRatedPk;
      patchObject.rating       = ratingIn;
      patchRatingFactor.put(patchObject).$promise.then(
          function(response) {
              toaster.pop('success', "Sėkmingai įvertinote!");
              $scope.getCurrentAvgRating($scope.Id);
          },
          function(rejection) {
              toaster.pop('error', "Nepavyko įvertinti");
              console.log(rejection);
          }
      );
    } else {
      patchObject.ratedOnBrand   = null;
      patchObject.ratedOnProduct = $scope.Id;
      patchObject.ratedById      = $scope.customerId;
      patchObject.rating         = ratingIn;
      patchObject.type           = 'P';
      postRatingFactor.create(patchObject).$promise.then(
          function(response) {
              toaster.pop('success', "Sėkmingai įvertinote!");
              $scope.alreadyRatedBool = true;
              $scope.alreadyRatedPk   = response.pk;
              $scope.getCurrentAvgRating($scope.Id);
          },
          function(rejection) {
              toaster.pop('error', "Nepavyko įvertinti");
              console.log(rejection);
          }
      );
    };
  };
  $scope.getCurrentAvgRating = function(productId){
    $http.get('/api/postrank/?ratedOnProduct=' + productId).then(function(response){
      var counter = 0;
      var sum = 0;
      for (var i = 0; i < response.data.length; i++){
        counter += 1;
        sum += response.data[i].rating;
      };
      if (counter > 0){
        $scope.currentAvgRating = (sum/counter).toFixed(1);
      };
    });
  };
  $scope.alreadyRated = function(productId, customer){
    $http.get('/api/postrank/?ratedOnProduct=' + productId + '&ratedById=' + customer).then(function(response){
      if (response.data[0] != undefined){
        $scope.alreadyRatedBool = true;
        $scope.alreadyRatedPk   = response.data[0].pk;
        $scope.currentRating    = response.data[0].rating.toString();
      }
    });
  };
  $scope.generateWarningsList = function(array)
  {
    for (var i = 0; i < array.length; i++){
      for (var j = 0; j < array[i].warnings.length; j++)
      if (!$scope.alreadyAdded($scope.warningsList, 'pk', array[i].warnings[j].pk))
      {
        $scope.warningsList.push(array[i].warnings[j]);
      };
    };
  };
  $scope.generateFunctionsList = function(array)
  {
    for (var i = 0; i < array.length; i++){
      for (var j = 0; j < array[i].functions.length; j++)
      if (!$scope.alreadyAdded($scope.functionsList, 'pk', array[i].functions[j].pk))
      {
        $scope.functionsList.push(array[i].functions[j]);
      };
    };
  };
  $scope.editTagLine = function(edit, newTagLine, id)
  {
    $scope.patchObject = {};
    $scope.tagLineEditMode = edit;
    $scope.patchObject.pk = id;
    if (edit == false &
        newTagLine !== undefined)
    {
      $scope.patchObject.tagLine = newTagLine;
      $scope.patchRecord($scope.patchObject);
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
  $scope.addIngredient = function(pk, name)
  {
    if ($scope.alreadyAdded($scope.attachedIngredients, 'pk', pk))
    {
      toaster.pop('error', "Ingredientas jau yra pridėtas");
    } else {
      $scope.attachedIngredients.push({pk, name});
      $scope.ingredientsChagned = true;
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
    $scope.ingredientsChagned = true;
  };
  $scope.editIngredients = function(edit, newTagLine, id)
  {
    $scope.patchObject = {};
    $scope.ingredientsEditMode = edit;
    $scope.patchObject.pk = id;
    if (edit == true)
    {
      $scope.attachedIngredients = $scope.productDetails.ingredients;
      $scope.search('');
    };
    if (edit == false)
    {
      if($scope.ingredientsChagned)
      {
        if ($scope.attachedIngredients.length > 0)
        {
          $scope.patchObject.ingredients = $scope.attachedIngredients.map(function(a) {return a.pk;});
          $scope.patchRecord($scope.patchObject);
          $scope.init($scope.customerId, '/api/product/');
        } else {
          $scope.init($scope.customerId, '/api/product/');
          toaster.pop('error', "Reikia pasirinkti bent vieną ingredientą");
        };
      };
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
          $scope.setPage(page, viaSearch, false);
          if ($scope.searchResults.count > 0){
            $scope.recordsExist = false;
          } else {
            $scope.recordsExist = true;
          };
        };
    });
  };
  $scope.setPage = function(page, viaSearch, comment){
    var tempPageList = [];
    if (typeof page !== 'number'){
      page = page.replace(/[^\d]/g, '');
    };
    if (comment){
      if (page == '' || page > $scope.commentsLastPage ||
         ($scope.commentsPageNo == page & !viaSearch)) {
        return false;
      };
      $scope.commentsPageNo   = page;
    } else {
      if (page == '' || page > $scope.lastPage ||
         ($scope.pageNo == page & !viaSearch)) {
        return false;
      };
      $scope.pageNo   = page;
    };

    tempPageList = ["<<" + page + ">>"];
    for (i = 1; i < 3; i++){
      if (page-i > 0){
        tempPageList.unshift(page-i);
      };
    };
    if (comment){
      for (i = 1; i < 3; i++){
        if (page+i <= $scope.commentsLastPage){
        tempPageList.push(page+i)
        };
      };
    } else {
      for (i = 1; i < 3; i++){
        if (page+i <= $scope.lastPage){
        tempPageList.push(page+i)
        };
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
    if (comment) {
      if (page+2 < $scope.commentsLastPage){
        tempPageList.push(" .. ");
        for (i = $scope.commentsLastPage - 1; i <= $scope.commentsLastPage; i++){
          if (i > page+1){
            tempPageList.push(i);
          };
        };
      };
      $scope.commentsPageList = tempPageList;
    } else {
      if (page+2 < $scope.lastPage){
        tempPageList.push(" .. ");
        for (i = $scope.lastPage - 1; i <= $scope.lastPage; i++){
          if (i > page+1){
            tempPageList.push(i);
          };
        };
      };
      $scope.pageList = tempPageList;
    }
    return true;
  };
  $scope.search = function(value){
     if (value !== undefined){
       $scope.value = value;
     };
     $scope.getSearchResults('/api/ingredients/', '?search=', $scope.value, 1, true);
  };
  $scope.anotherPage = function(page){
     if ($scope.setPage(page, false, false)){
       var action = "?page=" + page +"&search=";
       $scope.getSearchResults('/api/ingredients/', action, $scope.value, NaN, false);
     };
  };
  $scope.anotherCommentsPage = function(page){
     if ($scope.setPage(page, false, true)){
       var action = "?page=" + page +"&search=";
       $scope.getComments('/api/commentsproduct/', action, $scope.Id, page);
     };
  };
  $scope.getComments = function(url, action, value, page) {
     $http.get(url + action + value).then(function(response){
        $scope.commentsData = response.data;
        $scope.commentsLastPage = $scope.commentsData.count/10 >> 0;
        if (($scope.commentsData.count % 10) > 0){
          $scope.commentsLastPage += 1;
        };
        $scope.setPage(page, true, true);
    });
  };
  $scope.searchComments = function(action, value){
     $scope.getComments('/api/commentsproduct/', action, value, 1);
  };
  $scope.addComment = function(user, id)
  {
    if (user < 0) {
      toaster.pop('error', "Komentarą gali kurti tik registruoti naudotojai");
      $scope.noErrorsFound   = false;
      return;
    } else {
      $scope.comment.author = user;
    };
    $scope.errors = {};
    $scope.noErrorsFound = true;
    if ($scope.comment.tagLine == "" |
        $scope.comment.tagLine == undefined) {
      $scope.errors.tagLine = 'Įveskite komentarą';
      $scope.noErrorsFound   = false;
    };
    if ($scope.comment.youtube != undefined &&
      $scope.comment.youtube != '') {
      regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
      match = $scope.comment.youtube.match(regExp);
      if (match != null){
        if (match && match[2].length != 11) {
          $scope.errors.youtube = 'Youtube nuoroda nėra validi';
          $scope.noErrorsFound   = false;
        } else {
          $scope.comment.youtube  = match[2];
        };
      } else {
        $scope.errors.youtube = 'Youtube nuoroda nėra validi';
        $scope.noErrorsFound   = false;
      };
    };
    $scope.comment.commentedOnProduct = $scope.Id;
    if ($scope.noErrorsFound)
    {
      postComment.create($scope.comment).$promise.then(
          function(response) {
              toaster.pop('success', "Komentaras sukurtas!");
              $scope.comment = {};
              $scope.searchComments('?search=', id);
          },
          function(rejection) {
              toaster.pop('error', "Nepavyko sukurti komentaro..");
              console.log(rejection);
          }
      );
    } else {
      toaster.pop('error', "Komentaro formoje yra klaidų");
    };
  };
  $scope.getTrustedHTML = function(youtubeId){
    return "<iframe height=\"220px\" width=\"360\" src=\"http://www.youtube.com/embed/"+youtubeId+"\" allowfullscreen></iframe>";
  };
});
