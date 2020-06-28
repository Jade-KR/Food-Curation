export default [{
    path: "",
    view: "Home",
    name: "home"
  },
  {
    path: "/search",
    view: "Search",
    name: "search"
  },
  {
    path: "/register",
    view: "Register",
    name: "register"
  },
  {
    path: "/index",
    view: "index",
    name: "index"
  },
  {
    path: "/StoreDetail/:storeId",
    view: "StoreDetail",
    name: "StoreDetail"
  },
  {
    path: "/mypage/:userId",
    view: "Mypage",
    name: "mypage",
    meta: {
      authRequired: true
    }
  },
  {
    path: "*",
    view: "NotFound",
		name: "notFound",
	}
];