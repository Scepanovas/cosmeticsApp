mainApp.controller('ProfileCtrl', function($scope, $http, toaster, patchFactor,
                                           postComment, patchRatingFactor,
                                           postRatingFactor)
{
  $scope.patchRecord = function(patchObject)
  {
      patchFactor.put(patchObject).$promise.then(
          function(response) {
              toaster.pop('success', "Informacija atnaujinta!");
              if ($scope.profileDetails.tagLine != response.tagLine)
              {
                $scope.profileDetails.tagLine = response.tagLine;
              };
              if ($scope.profileDetails.country != response.country)
              {
                $scope.profileDetails.country = response.country;
              };
              if ($scope.profileDetails.webPage != response.webPage)
              {
                $scope.profileDetails.webPage = response.webPage;
              };
          },
          function(rejection) {
              toaster.pop('error', "Informacijos atnaujinti nepavyko");
              console.log(rejection);
          }
      );
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
  $scope.getId = function(url, customerId)
  {
    var urlLength = url.length;
    var urlLast   = url.lastIndexOf('/')+1;
    if (urlLength == urlLast)
    {
      url = url.substring(0,urlLength-1);
    };
    urlLast = url.lastIndexOf('/')+1;
    var id = url.substring(urlLast);
    if (!isNaN(id))
    {
      return id;
    } else if (id == "profilis" &
               customerId !== undefined)
    {
      id = customerId;
    } else
    {
      id = 0;
    };
    return id;
  };
  $scope.init = function(customerId)
  {
    $scope.currentRating = "";
    $scope.countryEditMode = false;
    $scope.tagLineEditMode = false;
    $scope.webPageEditMode = false;
    $scope.url = '/api/brands/';
    $scope.currentUrl = window.location.href;
    $scope.Id = $scope.getId($scope.currentUrl, customerId);
    $scope.customerId = customerId;
    $scope.profileExist = true;
    $scope.comment = {};
    $scope.alreadyRatedBool = false;
    $scope.currentAvgRating = 0;
    $scope.currentAvgRating = $scope.currentAvgRating.toFixed(1);
    if ($scope.Id == 0){
      $scope.profileExist = false;
    } else {
      $scope.alreadyRated($scope.Id, $scope.customerId);
      $scope.getCurrentAvgRating($scope.Id);
      if ($scope.Id == customerId){
        $scope.editable = true;
      };
      $http.get($scope.url + $scope.Id).then(function(response){
        $scope.profileDetails = response.data;
        if ($scope.profileDetails.webPage.substring(0, 6) == 'http://'){
          $scope.officialUrl = $scope.profileDetails.webPage;
        } else {
          $scope.officialUrl = 'http://' + $scope.profileDetails.webPage;
        };
        $scope.searchComments('?search=', $scope.Id);
        $scope.setPage(1, true, true);
      },
      function(data) {
        $scope.profileExist = false;
      });
    };
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
      patchObject.ratedOnBrand   = $scope.Id;
      patchObject.ratedOnProduct = null;
      patchObject.ratedById      = $scope.customerId;
      patchObject.rating         = ratingIn;
      if (brand) {patchObject.type = 'B';}
      else       {patchObject.type = 'U';};
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
  $scope.getCurrentAvgRating = function(profile){
    $http.get('/api/postrank/?ratedOnBrand=' + profile).then(function(response){
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
  $scope.alreadyRated = function(profile, customer){
    $http.get('/api/postrank/?ratedOnBrand=' + profile + '&ratedById=' + customer).then(function(response){
      if (response.data[0] != undefined){
        $scope.alreadyRatedBool = true;
        $scope.alreadyRatedPk   = response.data[0].pk;
        $scope.currentRating    = response.data[0].rating.toString();
      }
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
  $scope.editCountry = function(edit, newCountry, id)
  {
    $scope.patchObject = {};
    $scope.countryEditMode = edit;
    $scope.patchObject.pk = id;
    if (edit == false &
        newCountry !== undefined)
    {
      $scope.patchObject.country = newCountry;
      $scope.patchRecord($scope.patchObject);
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
  $scope.editWebPage = function(edit, newWebPage, id)
  {
    $scope.patchObject = {};
    $scope.webPageEditMode = edit;
    $scope.patchObject.pk = id;
    if (edit == false &
        newWebPage !== undefined)
    {
      $scope.patchObject.webPage = newWebPage;
      $scope.patchRecord($scope.patchObject);
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
     $scope.getComments('/api/commentsbrand/', action, value, 1);
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
    $scope.comment.commentedOnBrand = $scope.Id;
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
