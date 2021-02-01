use warp::Filter;

#[tokio::main]
async fn main() {

    let files = warp::path("static")
        .and(warp::fs::dir("./static"));

    warp::serve(files)
        .run(([127, 0, 0, 1], 5000))
        .await;
}
