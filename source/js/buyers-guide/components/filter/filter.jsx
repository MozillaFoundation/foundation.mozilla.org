import React from 'react';

/**
 * A simple class for radio-group-looking things.
 */
class RadioGroupEntry extends React.Component {
  constructor(props) {
    super(props);
  }

  forward(evt) {
    evt.preventDefault();
    evt.stopPropagation();
    this.props.onClick(this.props.label);
  }

  render() {
    return (
      <div onClick={e => this.forward(e)} className="radio-button">
        <span className={`dot` + (this.props.selected? ` selected`:``)}/> <span data-label={this.props.label} className={`label`}>{this.props.label}</span>
      </div>
    );
  }
}

/**
 * The homepage filter system
 */
export default class Filter extends React.Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
    this.setupDocumentListeners();
  }

  getInitialState() {
    return {
      collapsed: true,
      likelihood: `Both`,
      creepinessMin: 1,
      offsetMin: `calc(0% - 14px)`,
      creepinessMax: 100,
      offsetMax: `calc(100% - 14px)`,
      trackStyle: {}
    };
  }

  setupDocumentListeners() {
    this.moveListener = (function(evt) {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideMove(evt);
    }).bind(this);

    this.releaseListener = (function(evt) {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideReleased(evt);
      this.removeDocumentListeners();
    }).bind(this);
  }

  addDocumentListeners() {
    document.addEventListener('mousemove', this.moveListener, true);
    document.addEventListener('touchmove', this.moveListener, true);
    document.addEventListener('mouseup', this.releaseListener, true);
    document.addEventListener('touchstart', this.releaseListener, true);
  }

  removeDocumentListeners() {
    document.removeEventListener('mousemove', this.moveListener, true);
    document.removeEventListener('touchmove', this.moveListener, true);
    document.removeEventListener('mouseup', this.releaseListener, true);
    document.removeEventListener('touchstart', this.releaseListener, true);
  }

  open() {
    if (this.state.collapsed) {
      let update = {
        collapsed: false
      };

      this.updateWithCSSvalues(update);
      this.setState(update);
    }
  }

  close() {
    this.setState({ collapsed: true });
  }

  handleLikelihood(label) {
    this.setState({
      likelihood: label
    }, () => {
      this.setVisibilities();
    });
  }

  slideStart(e) {
    this.activeSlider = e.target;

    e.preventDefault();
    e.stopPropagation();

    this.setState({
      parentBBox: this.track.getBoundingClientRect(),
      dragging: true
    });

    // The "move" and "release" events have to be handled at
    // the document level, because the events can be generated
    // "nowhere near the React-managed DOM node".
    this.addDocumentListeners();
  }

  slideReleased() {
    this.activeSlider = false;

    this.setState({
      dragging: false
    });
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

      let fraction = (x-bbox.left)/bbox.width;
      let percentage = (fraction*100) | 0;
      let value = percentage ? percentage : 1;

      let update = {};
      let creepInterval = 10;

      if (this.activeSlider === this.minHead) {
        update.creepinessMin = Math.min(value, 100 - creepInterval);
        if (update.creepinessMin > this.state.creepinessMax - creepInterval) {
          update.creepinessMax = update.creepinessMin + creepInterval;
        }
      } else if(this.activeSlider === this.maxHead) {
        update.creepinessMax = Math.max(value, 1 + creepInterval);
        if (update.creepinessMax < this.state.creepinessMin + creepInterval) {
          update.creepinessMin = update.creepinessMax - creepInterval;
        }
      }

      this.updateWithCSSvalues(
        update,
        update.creepinessMin,
        update.creepinessMax
      );

      this.setState(update, () => {
        this.setVisibilities();
      });
    }
  }

  updateWithCSSvalues(update, min, max) {
    min = min || this.state.creepinessMin;
    max = max || this.state.creepinessMax;

    // TODO: update the faces as you slide

    if (this.track) {
      let bbox = this.track.getBoundingClientRect();

      if (bbox && bbox.width) {
        let interval = (max - min);

        update.offsetMin = `calc(${min}% - 14px)`;
        update.offsetMax = `calc(${max}% - 14px)`;

        update.trackStyle = {
          backgroundSize: `${interval}% 5px`,
          // TODO: compute this without having to resort to the bounding box.
          //
          // NOTE: computing this value based on percentages is INSANE, because
          // the background is positioned based on a double percentage: 0% will
          // anchor the left side of the background, to the left side of the
          // container, and 100% will anchor the right side of the background
          // to the right side of the container, regardless of the size of the
          // interval, so the behaviour is non-linear and things get super weird.
          backgroundPosition: `${Math.round(bbox.width * min/100)}px center`
        };
      }
    }
  }

  setVisibilities() {
    let minC = this.state.creepinessMin,
        maxC = this.state.creepinessMax,
        like = this.state.likelihood,
        all = Array.from(document.querySelectorAll(`.product-box`));

    all.forEach(productBox => {
      let c = parseInt(productBox.dataset.creepiness);
      let classes = productBox.classList;
      let keepChecking = true;

      // Filter out for creepiness
      if (c < minC || c > maxC) {
        classes.add(`d-none`);
        keepChecking = false;
      } else {
        classes.remove(`d-none`);
      }

      // not hidden by creepiness: do we need to hide it due to buyers likelihood?
      if (keepChecking) {
        let recommendation = productBox.querySelector(`.recommendation`);

        if (like === `Likely` && recommendation.classList.contains(`negative`)) {
          classes.add(`d-none`);
          keepChecking = false;
        } else if (like === `Not likely` && recommendation.classList.contains(`positive`)) {
          classes.add(`d-none`);
          keepChecking = false;
        }
      }

      // not hidden by recommendation: do we need to hide it due to seal-of-approval selection?
      if (keepChecking) {
        // ...code for this will go here
      }
    });
  }

  getFilterContent() {
    let mouseOpts = {
      onMouseDown: evt => this.slideStart(evt),
      onTouchStart: evt => this.slideStart(evt),
    };

    let likelihoods = [`Likely`, `Not likely`, `Both`].map(label => {
      return {
        label,
        onClick: label => this.handleLikelihood(label),
        selected: (this.state.likelihood === label)
      };
    });

    return (
      <div className={this.state.collapsed ? `d-none`: ``}>
        <span className="close" onClick={evt => this.close()} />

        <h2 className="h6-heading">Filter by</h2>

        <div className="creepiness">
          <h3 className="h6-heading">creepiness</h3>
          <div className="slider">
            <label>nice</label>
            <div className="track" ref={e => (this.track=e)} style={this.state.trackStyle}>
              <span className="min track-head" style={{ left: this.state.offsetMin }} ref={e => (this.minHead=e)} {...mouseOpts} />
              <span className="max track-head" style={{ left: this.state.offsetMax }} ref={e => (this.maxHead=e)} {...mouseOpts} />
            </div>
            <label className="creepy">creepy</label>
          </div>
        </div>

        <div className="likelihood">A simple class for radio-group-looking things.
          <h3 className="h6-heading">likelihood to buy</h3>
          { likelihoods.map(opts => <RadioGroupEntry {...opts}/>) }
        </div>
      </div>
    );
  }

  render() {
    let content = this.getFilterContent();
    return (
      <div
        className={`filter-content` + (this.state.collapsed ? ` collapsed` : ``)}
        onClick={evt => this.open()}
      >{ content }</div>
    );
  }
};
