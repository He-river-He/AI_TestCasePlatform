export function encodeCatalogKeyPart(value) {
  return encodeURIComponent(String(value ?? ''));
}

export function decodeCatalogKeyPart(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

export function makeModuleCatalogKey(module, prefix = '') {
  return `${prefix}m:${encodeCatalogKeyPart(module)}`;
}

export function makeFeatureCatalogKey(module, feature, prefix = '') {
  return `${prefix}m:${encodeCatalogKeyPart(module)}|f:${encodeCatalogKeyPart(feature)}`;
}

export function parseModuleFeatureCatalogKey(key) {
  if (!key) return null;
  const parts = String(key).split('|');
  const modulePart = parts.find((part) => part.startsWith('m:'));
  if (!modulePart) return null;
  const featurePart = parts.find((part) => part.startsWith('f:'));
  return {
    module: decodeCatalogKeyPart(modulePart.slice(2)),
    feature: featurePart ? decodeCatalogKeyPart(featurePart.slice(2)) : null,
  };
}
