function handler(event, ctx, cb) {
  console.log(JSON.stringify({ event }));
  cb(null, 'done');
}
module.exports = { handler };
