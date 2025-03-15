// vue.config.js
const fs = require("fs");
module.exports = {
  devServer: {
    https: {
      key: fs.readFileSync("localhost-key.pem"),
      cert: fs.readFileSync("localhost.pem"),
    },
    host: "localhost",
    port: 8080,
  }
};