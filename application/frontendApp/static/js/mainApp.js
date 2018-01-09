var mainApp = angular.module('mainApp',['ngResource',
  'toaster',
  'ngAnimate',
]);

mainApp.config(function($interpolateProvider) {
    //allow django templates and angular to co-exist
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});
mainApp.config(function($resourceProvider) {
    $resourceProvider.defaults.stripTrailingSlashes = false;

});
mainApp.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);
mainApp.filter('unsafe', function($sce) { return $sce.trustAsHtml; });

mainApp.factory('postComment', function($resource) {
    return $resource('/api/createcomment/:pk/', {'pk': '@pk'}, {
        'create': {
            method: 'POST',
        },
    });
});
mainApp.factory('createProductFactor', function($resource) {
    return $resource('/api/products/:pk/', {'pk': '@pk'}, {
        'create': {
            method: 'POST',
            transformRequest: transformImageRequest,
            headers: {'Content-Type':undefined}
        },
    });
});
mainApp.factory('patchProductFactor', function($resource) {
    return $resource('/api/products/:pk/', {'pk': '@pk'},{
        'put': {
            method: 'PATCH',
        },
    });
});
mainApp.factory('patchFactor', function($resource) {
    return $resource('/api/brands/:pk/', {'pk': '@pk'},{
        'put': {
            method: 'PATCH',
        },
        'update': {
            method: 'PATCH',
        },
    });
});
mainApp.factory('patchRatingFactor', function($resource) {
    return $resource('/api/postrank/:pk/', {'pk': '@pk'},{
        'put': {
            method: 'PATCH',
        },
    });
});
mainApp.factory('postRatingFactor', function($resource) {
    return $resource('/api/postrank/:pk/', {'pk': '@pk'},{
        'create': {
            method: 'POST',
        },
    });
});
mainApp.factory('RegisterFactor', function($resource) {
    return $resource('/api/brands/:pk/', {'pk': '@pk'}, {
        'create': {
            method: 'POST',
            transformRequest: transformImageRequest,
            headers: {'Content-Type':undefined}
        },
    });
});
