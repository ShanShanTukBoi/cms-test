const { createOAuthHandler } = require("netlify-cms-oauth-provider");

exports.handler = createOAuthHandler({
  site_id: process.env.SITE_ID,
});