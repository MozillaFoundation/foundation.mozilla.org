class NoOpStorage {
  clear() { }
  getItem() { }
  key() { }
  removeItem() { }
  setItem() { }
}

export default function getStorage(type) {
  let storage;
  try {
    storage = window[type];
    var x = '__storage_test__';
    storage.setItem(x, x);
    storage.removeItem(x);
    return storage;
  }
  catch (e) {
    return new NoOpStorage();
  }
}
