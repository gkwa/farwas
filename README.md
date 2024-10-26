# farwas - GitHub Repository Viewer

## Usage Examples

```bash
# Basic usage - view user repositories
farwas -u <username>

# View organization repositories
farwas -o <organization>

# Limit number of repositories shown
farwas -o <organization> --limit 100

# Different view formats
farwas -o <organization> view1  # Default format with descriptions
farwas -o <organization> view2  # Compact format with links
farwas -o <organization> view3  # Enhanced format with GitHub Actions status
farwas -o <organization> view4  # Actions-focused format with status sorting

# View cache contents
ls -la ~/.farwas/cache/

# Get help
farwas --help
```

## Views
- view1: Default format showing repository name, description, visibility and last update
- view2: Compact format with repository URLs for actions and commits
- view3: Enhanced format including latest GitHub Actions workflow status
- view4: Focused view of Actions status, sorted by:
  1. Failed workflows first
  2. Successful workflows second 
  3. Repositories without workflows last
  4. Within each group, sorted by most recent update

## Cache
- Cache location: ~/.farwas/cache/
- Cache timeout: 10 minutes
- Cache can be configured with --cache-dir flag

## Example view4 output

```bash
farwas --limit 20 --org myorg view4
```

```
failure      about 4 hours ago         https://github.com/myorg/repo1/actions
failure      about 4 hours ago         https://github.com/myorg/repo2/actions
success      about 4 hours ago         https://github.com/myorg/repo3/actions
success      about 4 hours ago         https://github.com/myorg/repo4/actions
no workflows about 9 minutes ago       https://github.com/myorg/repo5/actions
no workflows about 1 hours ago         https://github.com/myorg/repo6/actions
```