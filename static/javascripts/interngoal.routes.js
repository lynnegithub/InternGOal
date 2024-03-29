(function () {
	'use strict';

	angular
		.module('interngoal.routes')
		.config(config);

	config.$inject = ['$routeProvider'];

	/**
	* @name config
	* @desc Define valid application routes
	*/
	function config($routeProvider) {
		$routeProvider.when('/register', {
			controller: 'RegisterController',
			controllerAs: 'vm',
			templateUrl: '/static/templates/authentication/register.html'
		}).when('/login', {
			controller: 'LoginController',
			controllerAs: 'vm',
			templateUrl: '/static/templates/authentication/login.html'
		}).otherwise('/');
	}
})();