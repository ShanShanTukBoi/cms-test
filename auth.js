const { createOAuthHandler } = require("@decap-cms/oauth-provider-node");

exports.handler = createOAuthHandler({
  site_id: process.env.SITE_ID,
});