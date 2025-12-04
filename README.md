# FastAPI MongoDB Template

This repository contains an *opinionated* template for a FastAPI backend API with MongoDB as the no-SQL database.

It is primarily meant for my own personal use and thus contains features I've found useful over my *very limited* time developing backends.
However if you are nevertheless reading this, perhaps you have found this template useful and if so, I'd appreciate it if you left a star.

## Features

### Basics
- Implements a toy API where users can request to join organizations and organizations can invite users.
- **Pydantic** for schema validation.
- **Beanie** as an async object-document mapper (ODM) for MongoDB.
- **Github Actions** for CI/CD.
- **Pytest** for tests.

### Nginx Proxy Manager
Todo.

### Auth0
[Auth0](auth0.com) is a pretty popular platform for authentication, and this template contains [code](api/src/auth/auth0.py) to consume their JWT tokens.

However, backend auth is pretty useless without some metadata about the user (i.e. name and email) but in my opinion, it's just much easier to
include this information as a custom claim in the [access token](https://auth0.com/docs/secure/tokens/access-tokens)
rather than dealing with separate [ID tokens](https://auth0.com/docs/secure/tokens/id-tokens).
To support this, we must configure an Auth0 `post-login` [trigger](https://auth0.com/docs/customize/actions/explore-triggers) as follows. 

```javascript
/**
 * Handler that will be called during the execution of a PostLogin flow.
 *
 * @param {Event} event - Details about the user and the context in which they are logging in.
 * @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
 */
exports.onExecutePostLogin = async (event, api) => {
    // This action adds the authenticated user's email address to the access token.
    let namespace = event.secrets.NAMESPACE || '';
    if (namespace && !namespace.endsWith('/')) {
        namespace += '/';
    }
    api.accessToken.setCustomClaim(namespace + 'email', event.user.email);
    if (event.user.name) {
        api.accessToken.setCustomClaim(namespace + 'name', event.user.name);
    }
};
```


