import { Component } from "react";

/**
 * PNI creep-o-meter.
 * Displays a slider for voting.
 */
class Creepometer extends Component {
  constructor(props) {
    super(props);

    this.faceCount = 40; // Number of face frames
    this.faceHeight = 70; // pixel height for one frame
    this.framePath = `../../../../static/_images/buyers-guide/faces/`;

    this.state = {
      dragging: false,
      percentage: 50,
    };

    this.setupDocumentListeners();
  }

  componentDidMount() {
    if (this.props.whenLoaded) {
      this.props.whenLoaded();
    }
  }

  setupDocumentListeners() {
    this.moveListener = (evt) => {
      this.props.toggleMoved();
      evt.preventDefault();
      evt.stopPropagation();
      this.slideMove(evt);
    };

    this.releaseListener = (evt) => {
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
      dragging: true,
    });

    // The "move" and "release" events have to be handled at
    // the document level, because the events can be generated
    // "nowhere near the React-managed DOM node".
    this.addDocumentListeners();
  }

  slideReleased() {
    this.setState({
      dragging: false,
    });
  }

  slideFromKey(e) {
    const k = e.key;
    let p = this.state.percentage;
    if (k === `ArrowLeft`) {
      this.saveTrackHead(p - 5);
    }
    if (k === `ArrowRight`) {
      this.saveTrackHead(p + 5);
    }
  }

  slideFromClick(e) {
    let x = e.clientX;

    if (e.touches) {
      x = e.touches[0].clientX;
    }

    this.repositionTrackHead(x, this.sliderElement.getBoundingClientRect());
  }

  slideMove(e) {
    if (this.state.dragging) {
      let x = e.clientX,
        bbox = this.state.parentBBox;

      if (e.touches) {
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
    let percentage = Math.round((100 * (x - bbox.left)) / bbox.width);
    this.saveTrackHead(percentage);
  }

  saveTrackHead(percentage = 1) {
    if (percentage < 1) percentage = 1;
    if (percentage > 100) percentage = 100;
    this.setState({ percentage }, () => {
      if (this.props.onChange) {
        this.props.onChange(percentage);
      }
    });
  }

  render() {
    let frameOffset = Math.round(
      (this.state.percentage * (this.faceCount - 1)) / 100
    );

    let trackheadOpts = {
      style: {
        left: `${this.state.percentage}%`,
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
      onMouseDown: (evt) => this.slideStart(evt),
      onTouchStart: (evt) => this.slideStart(evt),
    };

    return (
      <div className="creepometer">
        <div className="slider-container p-2">
          <div
            className="slider"
            ref={(e) => (this.sliderElement = e)}
            tabIndex="0"
            role="slider"
            onClick={(evt) => this.slideFromClick(evt)}
            onKeyDown={(evt) => this.slideFromKey(evt)}
            aria-valuemax={100}
            aria-valuemin={1}
            aria-valuenow={this.state.percentage}
            aria-label="Please indicate how creepy you think this product is on a scale from 0 (not creepy at all) to 100 (incredibly creepy)"
          >
            <div className="body-small copy copy-left">Not creepy</div>
            <div className="trackhead" {...trackheadOpts}>
              <div className="face" {...faceOpts} {...mouseOpts} />
              <div className="pip" {...mouseOpts} />
            </div>
            <div className="body-small copy copy-right">Super creepy</div>
          </div>
        </div>
      </div>
    );
  }
}

export default Creepometer;
