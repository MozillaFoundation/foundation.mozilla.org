class NoopStorage {
  clear() {}
  getItem() {}
  key() {}
  removeItem() {}
  setItem() {}
}

const haveWindow = typeof window !== "undefined";

const Storage = {
  localStorage: haveWindow ? window.localStorage : new NoopStorage(),
  sessionStorage: haveWindow ? window.sessionStorage : new NoopStorage(),
};

export default Storage;
