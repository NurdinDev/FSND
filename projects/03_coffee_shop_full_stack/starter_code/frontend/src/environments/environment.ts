export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-w8atoo8w.eu', // the auth0 domain prefix
    audience: 'http://127.0.0.1:5000', // the audience set for the auth0 app
    clientId: 'H6GgibcgtK1DPfP2zeozAJcpEICKpHmo', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application.
  }
};