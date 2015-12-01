(function () {
	'use strict';

	angular
  		.module('interngoal', [
  			'interngoal.authentication',
        'interngoal.config',
        'interngoal.layout',
  			'interngoal.routes',
  		]);

  	angular
  		.module('interngoal.config', []);

  	angular
  		.module('interngoal.routes', ['ngRoute']);

  	// CSRF PROTECTION
  	angular
  		.module('interngoal')
  		.run(run);

  	run.$inject = ['$http'];

  	/**
  	* @nam run
  	* @desc Update xsrf $http headers to align with Django's defaults
  	*/
  	function run($http) {
  		$http.defaults.xsrfHeaderName = 'X-CSRFToken';
  		$http.defaults.xsrfCookieName = 'csrftoken';
  	}
})();