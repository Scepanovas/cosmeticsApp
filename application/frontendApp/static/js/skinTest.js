mainApp.controller('SkinTestCtrl', function($scope, $http, toaster, patchFactor)
{
  $scope.init = function(url, userId)
  {
    $scope.url             = url + userId.toString();
    $scope.userId          = userId;
    $scope.answers         = {};
    $scope.currentSkinType = "Nenustatytas";
    $scope.takeTestLbl     = "Testo pradžia";
    $scope.getDetails($scope.url);
  };
  $scope.changeSign = function(showDetails, id)
  {
    if (showDetails)
    {
      document.getElementById(id).innerHTML = "-";
    } else {
      document.getElementById(id).innerHTML = "+";
    };
  };
  $scope.getDetails = function(url)
  {
    $http.get(url).then(function(response){
      $scope.userDetails = response.data;
      if ($scope.userDetails.skinType != null)
      {
        $scope.currentSkinType = $scope.userDetails.skinType.name;
      };
    });
  };
  $scope.saveTestResults = function()
  {
    $scope.noErrorsFound = true;
    $scope.errors        = {};
    $scope.patchObject   = {};

    if (typeof $scope.answers.age === 'undefined') {
      $scope.errors.age = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.water === 'undefined') {
      $scope.errors.water = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.surounding === 'undefined') {
      $scope.errors.surounding = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.hours === 'undefined') {
      $scope.errors.hours = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.uv === 'undefined') {
      $scope.errors.uv = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.plane === 'undefined') {
      $scope.errors.plane = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.skin === 'undefined') {
      $scope.errors.skin = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.concern1 === 'undefined') {
      $scope.errors.concern1 = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.concern2 === 'undefined') {
      $scope.errors.concern2 = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.concern1 !== 'undefined' &&
        typeof $scope.answers.concern2 !== 'undefined' &&
        $scope.answers.concern1 == $scope.answers.concern2) {
      $scope.errors.concern2 = 'Antras aspektas negali sutapti su pirmuoju';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.answers.rash === 'undefined') {
      $scope.errors.rash = 'Nepasirinkote atsakymo';
      $scope.noErrorsFound   = false;
    };
    if (!$scope.noErrorsFound){
      toaster.pop('error', "Teste yra klaidų");
      return;
    };
    var resultsString = $scope.answers.age + $scope.answers.water +
                        $scope.answers.surounding + $scope.answers.hours +
                        $scope.answers.uv + $scope.answers.plane +
                        $scope.answers.skin + $scope.answers.concern1 +
                        $scope.answers.concern2 + $scope.answers.rash;
    var dry          = resultsString.replace(/[^s]/g, "").length;
    var normal       = resultsString.replace(/[^n]/g, "").length;
    var oily         = resultsString.replace(/[^r]/g, "").length;
    var rash         = resultsString.replace(/[^b]/g, "").length;
    var sensitive    = resultsString.replace(/[^u]/g, "").length;
    var red          = resultsString.replace(/[^q]/g, "").length;
    var damagedBySun = resultsString.replace(/[^z]/g, "").length;
    var tired        = resultsString.replace(/[^p]/g, "").length;

    if ((oily+oily*0.28) > dry &&
        (oily+oily*0.28) > (normal+normal*0.4)){
      switch(rash) {
        case 6:
        case 5:
        case 4:
          $scope.userTempSkinType = 2;
          break;
        case 3:
        case 2:
          $scope.userTempSkinType = 4;
          break;
        default:
          if (sensitive == 0) {$scope.userTempSkinType = 3;}
          else                {$scope.userTempSkinType = 5;};
      };
    } else if (dry > (normal+normal*0.4) &&
               dry > (oily+oily*0.28)) {
        if (damagedBySun == 2)                {$scope.userTempSkinType = 9}
        else if (tired > (sensitive+red)*2/3) {$scope.userTempSkinType = 8}
        else                                  {$scope.userTempSkinType = 10};
    } else {
      if (sensitive == 0 &&
          red       == 0) {$scope.userTempSkinType = 7;}
      else                {$scope.userTempSkinType = 6;}
    };
    $scope.patchObject.isTested    = true;
    $scope.patchObject.pk          = $scope.userId;
    $scope.patchObject.skinType    = $scope.userTempSkinType;
    patchFactor.put($scope.patchObject).$promise.then(
        function(response) {
            toaster.pop('success', "Odos tipas nustatytas sėkmingai!");
            $scope.currentSkinType = response.skinType.name;
            $scope.showDetails     = false;
            $scope.answers         = {};
            document.getElementById('sign').innerHTML = "+";
            $scope.getDetails($scope.url);
        },
        function(rejection) {
            toaster.pop('error', "Nepavyko nustatyti odos tipo");
            console.log(rejection);
        }
    );
  };

});
