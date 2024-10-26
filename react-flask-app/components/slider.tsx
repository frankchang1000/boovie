import React from "react";
import Carousel from "react-multi-carousel";
import "react-multi-carousel/lib/styles.css";
import classes from "../css/slider.module.css";
const responsive = {
  desktop: {
    breakpoint: { max: 3000, min: 1024 },
    items: 4,
    slidesToSlide: 4, // optional, default to 1.
  },
  tablet: {
    breakpoint: { max: 1024, min: 768 },
    items: 3,
    slidesToSlide: 3, // optional, default to 1.
  },
  mobile: {
    breakpoint: { max: 767, min: 464 },
    items: 2,
    slidesToSlide: 1, // optional, default to 1.
  },
};
const sliderImageUrl = [
  //First image url
  {
    url: "../imgs/1984.jpg",
  },
  {
    url: "../imgs/harrypotter.jpg",
  },
  {
    url: "../imgs/percyjackson.jpg",
  },
  {
    url: "../imgs/tkam.jpg",
  },
  {
    url: "../imgs/thegiver.jpg",
  },
  {
    url: "../imgs/eragon.jpg",
  },
  {
    url: "../imgs/fahrenheit451.jpg",
  },
  {
    url: "../imgs/lotf.jpg",
  },
  {
    url: "../imgs/bookthief.jpg",
  },
];
const Slider = () => {
  return (
    <div className={classes.parent}>
      <div className={classes.sliderContainer}>
        <Carousel
          responsive={responsive}
          autoPlay={true}
          swipeable={true}
          draggable={true}
          showDots={true}
          infinite={true}
          partialVisible={false}
          dotListClass="custom-dot-list-style"
        >
          {sliderImageUrl.map((imageUrl, index) => {
            return (
              <div className={classes.slider} key={index}>
                <img src={imageUrl.url} alt="movie" />
              </div>
            );
          })}
        </Carousel>
      </div>
    </div>
  );
};
export default Slider;
