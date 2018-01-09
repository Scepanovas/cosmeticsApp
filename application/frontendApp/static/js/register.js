mainApp.controller('RegisterCtrl', function($scope, $http, RegisterFactor, toaster)
{
  $scope.init = function()
  {
    $scope.registerModel = {'country':"", 'tagLine':"",'brandName':"", 'webPage':"", 'isBrand':false};
    $scope.url = '/api/brands/?search=';
  };
  $scope.alreadyExist = async function(url, value)
  {
    const result = await $http.get(url + value);
    return (result.data.length > 0);
  };
  $scope.validEmail = function(email)
  {
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
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
  $scope.postRegistration = function(form)
  {
      RegisterFactor.create(form).$promise.then(
          function(response) {
              toaster.pop('success', "Paskyra sėkmingai sukurta!");
              document.getElementById("username").value = form.username;
              document.getElementById("password").value = form.password;
              $("#login-form").submit();
          },
          function(rejection) {
              toaster.pop('error', "Registracija nepavyko");
              console.log(rejection);
          }
      );
  };
  $scope.register = async function()
  {
    $scope.errors = {};
    $scope.noErrorsFound = true;
    if (typeof $scope.registerModel.username === 'undefined') {
      $scope.errors.username = 'Registruojant naudotoją privaloma įvesti slapyvardį';
      $scope.noErrorsFound   = false;
    } else {
      if ($scope.registerModel.username.length > 4)
      {
        if (await $scope.alreadyExist($scope.url, $scope.registerModel.username))
        {
          $scope.errors.username = 'Naudotojas su tokiu vardu jau egzistuoja';
          $scope.noErrorsFound   = false;
        } else if ($scope.registerModel.username.search(" ") > -1)
        {
          $scope.errors.username = 'Naudotojo varde negalima naudoti tarpų';
          $scope.noErrorsFound   = false;
        };
      } else {
        $scope.errors.username = 'Naudotojo vardą turi sudaryti bent 5 ženklai';
        $scope.noErrorsFound   = false;
      };
    };
    if (typeof $scope.registerModel.password === 'undefined')
    {
      $scope.errors.password = 'Registruojant naudotoją privaloma įvesti slaptažodį';
      $scope.noErrorsFound   = false;
    }
    else if ($scope.registerModel.password.length < 5)
    {
      $scope.errors.password = 'Slaptažodis turi sudaryti bent 5 ženklai';
      $scope.noErrorsFound   = false;
    };
    if (typeof $scope.registerModel.email === 'undefined') {
      $scope.errors.email = 'Registruojant naudotoją privaloma įvesti el. pašto adresą';
      $scope.noErrorsFound   = false;
    } else {
      if ($scope.validEmail($scope.registerModel.email))
      {
        if (await $scope.alreadyExist($scope.url, $scope.registerModel.email))
        {
          $scope.errors.email = 'Toks el. paštas jau yra registruotas';
          $scope.noErrorsFound   = false;
        }
      } else {
        $scope.errors.email = 'El. pašto adresas nėra validus';
        $scope.noErrorsFound   = false;
      };
    };
    if (typeof $scope.myFile !== 'undefined') {
      if ($scope.myFile.type.substring(0,5) == "image")
      {
        $scope.registerModel.image = $scope.myFile;
      } else {
        $scope.errors.image = 'Netinkamas paveikslėlio tipas';
        $scope.noErrorsFound   = false;
      }
    }
    else
    {
      $scope.errors.image = 'Pridėkite paveikslėlį';
      $scope.noErrorsFound   = false;
    }
    if ($scope.registerModel.isBrand)
    {
      if (typeof $scope.registerModel.brandName === 'undefined') {
        $scope.errors.brandName = 'Registruojant prekės ženklą privaloma įvesti pavadinimą';
        $scope.noErrorsFound   = false;
      } else {
        if ($scope.registerModel.brandName.length < 5) {
          $scope.errors.brandName = 'Pavadinimą turi sudaryti bent 5 ženklai';
          $scope.noErrorsFound   = false;
        }
        else if (await $scope.alreadyExist($scope.url, $scope.registerModel.brandName))
        {
          $scope.errors.brandName = 'Toks pavadinimas jau egzistuoja.';
          $scope.noErrorsFound   = false;
        };
      };
    };

    $scope.safeApply($scope);
    if ($scope.noErrorsFound)
    {
      $scope.postRegistration($scope.registerModel);
    } else {
      toaster.pop('error', "Registracijos formoje yra klaidų");
    };
  };
});
