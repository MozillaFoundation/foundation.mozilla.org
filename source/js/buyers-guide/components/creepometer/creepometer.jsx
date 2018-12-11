import React from 'react';

export default class Creepometer extends React.Component {
  constructor(props) {
    super(props);

    this.faceCount = 40; // Number of face frames
    this.faceHeight = 70; // pixel height for one frame
    this.framePath = `/_images/buyers-guide/faces/`;

    this.state = {
      dragging: false,
      percentage: 50,
      value: 50
    };

    this.setupDocumentListeners();
  }

  setupDocumentListeners() {
    this.moveListener = evt => {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideMove(evt);
    };

    this.releaseListener = evt => {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideReleased(evt);
      this.removeDocumentListeners();
    };
  }

  addDocumentListeners() {
    document.addEventListener(`mousemove`, this.moveListener, true);
    document.addEventListener(`touchmove`, this.moveListener, true);
    document.addEventListener(`mouseup`, this.releaseListener, true);
    document.addEventListener(`touchstart`, this.releaseListener, true);
  }

  removeDocumentListeners() {
    document.removeEventListener(`mousemove`, this.moveListener, true);
    document.removeEventListener(`touchmove`, this.moveListener, true);
    document.removeEventListener(`mouseup`, this.releaseListener, true);
    document.removeEventListener(`touchstart`, this.releaseListener, true);
  }

  slideStart(e) {
    e.preventDefault();
    e.stopPropagation();

    this.setState({
      parentBBox: this.sliderElement.getBoundingClientRect(),
      dragging: true
    });

    // The "move" and "release" events have to be handled at
    // the document level, because the events can be generated
    // "nowhere near the React-managed DOM node".
    this.addDocumentListeners();
  }

  slideReleased() {
    this.setState({
      dragging: false
    });
  }

  slideClick(e) {
    let x = e.clientX;

    if (e.touches) {
      x = e.touches[0].clientX;
    }

    this.repositionTrackHead(x, this.sliderElement.getBoundingClientRect());
  }

  slideMove(e) {
    if (this.state.dragging) {
      let x = e.clientX, bbox = this.state.parentBBox;

      if (e.touches){
        x = e.touches[0].clientX;
      }

      // cap the position:
      if (x > bbox.right) {
        x = bbox.right;
      } else if (x < bbox.left) {
        x = bbox.left;
      }

      this.repositionTrackHead(x, bbox);
    }
  }

  repositionTrackHead(x, bbox) {
    // compute the handle offset
    let percentage = Math.round(100 * (x - bbox.left) / bbox.width);
    let value = percentage ? percentage : 1;

    this.setState({
      percentage,
      value
    }, () => {
      if (this.props.onChange) {
        this.props.onChange(value);
      }
    });
  }

  render() {
    let frameOffset = Math.round(this.state.percentage * (this.faceCount-1)/100);

    let trackheadOpts = {
      style: {
        left: `${this.state.value}%`
      },
    };

    let faceOpts = {
      style: {
        background: `url("${this.framePath}sprite-resized-64-colors.png"), #f2b946`,
        backgroundSize: `70px`,
        backgroundPositionX: 0,
        backgroundPositionY: `-${frameOffset * this.faceHeight}px`,
        backgroundRepeat: `no-repeat`,
      },
    };

    let mouseOpts = {
      onMouseDown: evt => this.slideStart(evt),
      onTouchStart: evt => this.slideStart(evt),
    };

    return (
      <div className="creepometer">
        <div className="slider-container p-2">
          <div className="slider" ref={e => (this.sliderElement=e)} onClick={evt => this.slideClick(evt)}>
            <div className="h6-heading copy copy-left">Not creepy</div>
            <div className="trackhead" {...trackheadOpts}>
              <div className="face" {...faceOpts} {...mouseOpts}/>
              <div className="pip" {...mouseOpts}/>
            </div>
            <div className="h6-heading copy copy-right">Super creepy</div>
          </div>
        </div>
      </div>
    );
  }
}
